# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import requests
import mysql.connector
from celebrityindian.items import CelebrityindianItem
import bs4 as bs;
from urllib.request import Request, urlopen

class CelebritySpider(CrawlSpider):
    name = 'celebrity'
    celebrityCount = 1;
    allowed_domains = ['in.bookmyshow.com']
    start_urls = ['https://in.bookmyshow.com/entertainment/movies/hindi/']

    #Extract Links for Navigation
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.next.page-numbers',)),
             callback="parse_item",
             follow=True),)
    
    #Parse Links for navigating to Celebrities Page
    def parse_item(self, response):
        #Fetch Item Links for navigating to Celebrities Page
        item_links = response.selector.xpath('//h2//a/@href').extract()
        #Fetch Item Links title for further filter
        item_title = response.selector.xpath('//h2//a/text()').extract()
        
        #Which url currently processing
        print("processing:"+response.url)
        
        #Filter Item Links for Celebrity pages
        Filtered_itemlinks = self.filterLinks(item_title,item_links)
        
        #Call for filtered links for further detail parsing
        for a in Filtered_itemlinks:
            print("alink")
            print(a);
            yield scrapy.Request(a, callback=self.parse_detail_page)
        
        
    #Parse celebrity page for saving details of celebrities
    def parse_detail_page(self, response):
       
        #extract Names of Celebrities from Page
        name = self.extractNames(response)
        
        #Remove digits and other symbols from Names
        name = self.extractnumbers(name);
        
        #extract Personality of Celebrities from respective page
        description = self.extractDescription(response)
        
        #extract Picture link from page
        imgSrc = response.selector.xpath('//figure//img/@src').extract()
        print(name)
        print(imgSrc)
        
        #extract Picture from link and save Data in Database
        self.extractImagesandSaveData(imgSrc,name,description);
        
                
        #Save Data in JSON page as well
        item = CelebrityindianItem()
        item['name'] = name
        item['personality'] = description
        item['url'] = response.url
        yield item


    #extract Picture from link and save Data in Database
    def extractImagesandSaveData(self,imgSrc,name,description):
        i=0;
        #connect to MySQL Database
        connection = self.connectDatabase();
        for img in imgSrc:
            filename = 'images/'+img.split("/")[-1]
            rawImage = requests.get(img, stream=True)
                
            with open(filename, 'wb') as fd:
                for chunk in rawImage.iter_content(chunk_size=1024):
                    fd.write(chunk)
           
            self.saveData(connection, filename,name[i],description[i]);
            i=i+1;
        #Close connection
        connection.close();
    
    
    #Filter Item Links for Celebrity pages
    def filterLinks(self,item_title,item_links):
        i=0;
        Filtered_itemlinks=[];
        for a in item_title:
           if a.find("Bollywood") >= 0 and (a.find("Celebrities") >= 0 or a.find("Celebs") >= 0) and a.find("Movies") < 0 or (a.find("Actresses") >= 0 and a.find("90s") >= 0):
                print(a)
                Filtered_itemlinks.append(item_links[i])
           i=i+1;
        return Filtered_itemlinks;
    
    
    #Connect to MySQL Database
    def connectDatabase(self):
        connection = mysql.connector.connect(host='localhost',
                                             database='Celebrity',
                                             user='root',
                                             password='root')
        
        return connection
    
    
    #Save Data in Database
    def saveData(self,connection,fileName,name,description):
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO CelebrityDetail
                          (id, Name, Picture, Personality) VALUES (%s,%s,%s,%s)"""

        celebrityPicture = self.convertToBinaryData(fileName)
        id = self.celebrityCount;
        
        insert_blob_tuple = (id, name, celebrityPicture, description)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        self.celebrityCount = self.celebrityCount+1;
        print("Image and file inserted successfully as a BLOB into python_employee table", result)
        
        
    #Convert Picture into Binary Data
    def convertToBinaryData(self,filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData 
            
        
    #Remove digits and other symbols from Names
    def extractnumbers(self,name):
        updatedNameList = []
        for s in name:
            s = ''.join([i for i in s if not i.isdigit() and i != '.' 
                         and i != ')'])
            updatedNameList.append(s)    
        
        return updatedNameList;
        
    #extract Names of Celebrities from Page
    def extractNames(self,response):
        name = [
        ' '.join(
            line.strip() 
            for line in p.xpath('.//text()').extract() 
            if line.strip()
        ) 
        for p in response.xpath('//h2')
        ]
        return name
    
    #extract Personality of Celebrities from Page
    def extractDescription(self,response):
     
        req = Request(response.url, headers={'User-Agent': 'Mozilla/5.0'})
        sauce = urlopen(req).read()
        soap = bs.BeautifulSoup(sauce,'lxml')
        h2 = soap.findAll('h2')
        
        description=[];
        
        for h in h2:
            str = '';
            for p in h.findNextSiblings():
                if p.name=='h2':
                    break;
                if p.name=='p':
                    str += p.getText()
                    #print(str)
            description.append(str);
        
        return description;
        
        
        
        
        
        

