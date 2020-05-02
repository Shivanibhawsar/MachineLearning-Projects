import boto3
import io
import cv2 as cv
import re;
import os;
import glob;
from PIL import Image, ImageDraw, ImageFont
import datetime;
from dateutil.parser import parse
import numpy as np
import pandas as pd

#Fetch Detail and Save in Excel 
def fetchData():
    #List of Labels for Header in Esxcel
    columnList = ['Licence Number','ChasisNumber','EngineNumber','Name','RegistrationDate','ManufacturingDate','FileName']
    #initialize DataFrame for saving data
    df = pd.DataFrame(columns = columnList)
    
    #fetch all Image files from RC folder
    for file in glob.iglob('RC/*', recursive=True):
        print(file)
        bucket=''
        
        #Dictionary to save fetched Data
        dataList = {}
        
        #Process Image before Analysis
        file,image,image_binary = processImage(file)
        
        #Call AWS Textract API for detecting words and further extract meaningful data using raw words
        block_count, dataList = process_text_analysis(bucket,image,image_binary,dataList)
       
        #Save Fetched data to Excel
        df = savetoExcel(dataList,df,columnList,file)
    

#Save Fetched Data from dataList  dictionary to Excel named as FinalRCData
def savetoExcel(dataList,df,columnList,file): 
    #List for saving fetched data for specific image
    valuesList = []
    #Iterate over list and save data
    for column in columnList:
        if column in dataList:
            valuesList.append(dataList[column])
        elif column == 'FileName':
            valuesList.append(file)
        else:
            valuesList.append('N/A')
    
    df = df.append(pd.Series(valuesList, index=columnList), ignore_index=True)
    df.to_excel('FinalRCData.xlsx');
    return df;
    
    
    

def processImage(filename):
    #if ImageType is 'JPG' then convert to PNG and delete JPG file
    if(filename[-3:] == 'jpg'):
        im = Image.open(filename).convert("RGB")
        im.save(filename[:-4]+'new'+'.png','PNG')
        os.remove(filename)
        filename = filename[:-4]+'new'+'.png';
    #byteImg = sharpenImage(filename);
        
    #convert image to bytes    
    byteImgIO = io.BytesIO()
    byteImg = Image.open(filename).convert("RGB")
    byteImg.save(byteImgIO, "PNG")
    byteImgIO.seek(0)
    byteImg = byteImgIO.read()
    
    stream = io.BytesIO(byteImg)
    image=Image.open(stream)
    image_binary = stream.getvalue()
    
    return filename , image, image_binary


#Sharpen Image for blurred images
def sharpenImage(filename):
    image = cv.imread(filename)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    #sharpen_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    sharpen = cv.filter2D(image, -1, sharpen_kernel)
    #cv.imshow('sharpen', sharpen)
    success, encoded_image = cv.imencode('.png', sharpen)
    byteImg = encoded_image.tobytes()
    
    return byteImg;


# Detect Required Data using there Structure Logic
def DetectRCData(block,dataList,prevText,dicflag,dicname):
    
    
    if 'Text' in block:
        #for ':' , model detecting 'I' and needed to be skipped
        if(block['Text'] != 'I' and block['Text'] != '-'):
            #detect Chasis, Engine, Licence Number 
            dataList = detectChasis_Engine_Licence_Number(block['Text'],dataList,prevText)
            
            #detect Registration and Manufacturing Date
            dataList = detectRegandMFGDate(block['Text'],dataList,prevText)
            
            #detect Name
            dicflag,dicname,dataList = detectName(block['Text'],dataList,prevText,dicflag,dicname)
            
            #updating Previous Text
            prevText = block['Text'];
        
    return dataList, prevText,dicflag,dicname;


#detect Chasis, Engine and Licence Number 
def detectChasis_Engine_Licence_Number(detectedText,dataList,prevText):
    #check for Structure of Licence Number
    if(('No.' == prevText or 'NO' == prevText or 'I' == prevText or (len(prevText)==5 and prevText[0:2] == 'HR') ) and ((len(detectedText) == 10 and (detectedText[0:2] == 'DL' or detectedText[0:2] == 'HR')) or
           (len(detectedText) == 11 and detectedText[0:2] == 'HR'))
       ):
        dataList.update({'Licence Number' : detectedText})
    elif(len(prevText)==5 and (prevText[0:2] == 'HR' or prevText[0:2] == 'DL')and len(detectedText) == 4):
        dataList.update({'Licence Number' : prevText+detectedText})
    elif( 'Licence' in prevText and len(detectedText) == 5 ):
        dataList.update({'Licence Number' : detectedText})
        
    #check for Chasis Number Structure
    elif(( 'No.' == prevText or 'No,' == prevText  or 'NO' == prevText or 'CH.NO' == prevText  or 'NO' == prevText ) 
       and ( (len(detectedText) == 17 and detectedText[0:2] == 'MA') or (len(detectedText) == 15 and detectedText[0:2] != 'MA') or (len(detectedText) == 19 and '*' in detectedText ) ) ):
        dataList.update( {'ChasisNumber' : detectedText} )
    
    #check for Engine Number Structure
    elif(('No.' == prevText or 'ENO' == prevText or 'NO' == prevText  or 'Engine' == prevText) and len(detectedText) > 5  and  (detectedText.isalpha() == False ) ):
        dataList.update( {'EngineNumber' : detectedText} )
        
    return dataList;
    

# Detect Registration and Manufacturing Date
def detectRegandMFGDate(detectedText,dataList,prevText):
    #check for Registration Date
    if(('Issue' in prevText or 'DT' in prevText ) and is_date(detectedText) and validate(detectedText,'%d/%m/%Y')):
        dataList.update( {'RegistrationDate' : detectedText} );
    #check for Manufacturing Date
    elif((('Manufacture' in prevText or 'DT' in prevText or 'MFG.DT' in prevText or 'MFG.DT' in prevText or 'MFG.DT.' in prevText) and is_date(detectedText) and validate(detectedText,'%m/%Y')) or ('Manufacture' in prevText and is_date(detectedText) and validate(detectedText,'%d/%m/%Y'))):
        dataList.update( {'ManufacturingDate' : detectedText} );
    
    return dataList;

#check if string is valid date
def is_date(string, fuzzy=False):
    #print(string)
    try: 
        parse(string, fuzzy=fuzzy)
        #print(infer([string]))
        return True
    except(Exception):
        return False

#check format of date
def validate(date_text,dateformat):
    try:
        datetime.datetime.strptime(date_text, dateformat)
        return True
    except Exception:
        return False

#detect Name 
def detectName(detectedText,dataList,prevText,dicflag,dicname):
    iden = '1'
    dicflag,dicname,dataList = checkNAMErange(detectedText,dataList,prevText,dicflag,dicname,'NAME','SAWID',iden);
    iden = '2'
    dicflag,dicname,dataList = checkNAMErange(detectedText,dataList,prevText,dicflag,dicname,'Name','Address',iden);
    iden = '3'
    dicflag,dicname,dataList = checkNAMErange(detectedText,dataList,prevText,dicflag,dicname,'Address','of',iden);
    iden = '4'
    dicflag,name,dataList = checkNAMErange(detectedText,dataList,prevText,dicflag,dicname,'Name','SADIW',iden);
    iden = '5'
    dicflag,dicname,dataList = checkNAMErange(detectedText,dataList,prevText,dicflag,dicname,'NAME','SWID',iden);
    
    return dicflag,dicname,dataList;

#detect Name(Using Surrounding words logic)
def checkNAMErange(detectedText,dataList,prevText,dicflag,dicname,keyname,valuename,iden):
    
    if( keyname == prevText):
        dicflag[iden] = True;
    listSON = ['S/DA','SAID','S/WID','S/D/', 'SIID','SIWID','SIIID','SANTD','S/DW','S/ID','SWWID' ,'S/DOf']
    if(valuename == detectedText or detectedText in listSON ):
        
        dicflag[iden]= False;
       
    elif(dicflag[iden] == True):
        if('and' in detectedText):
            dicname[iden] = dicname[iden] + ' ';
        else:
            dicname[iden] = dicname[iden] + ' ' + detectedText;
      
    dicnamelist = dicname[iden].split();
    
    if(len(dicname[iden].split()) > 4):
        if(dicnamelist[0]=='I'):
             dicname[iden] = dicname[iden].split(' ', 1)[1]
        else:
            dicflag[iden]= False;
            dicname[iden] = '';
            
    return dicflag,dicname,dataList;



#Using AWS Textract to fetch raw detected words
def process_text_analysis(bucket, image,image_binary,dataList): 
    
    
    # Analyze the document
    client = boto3.client('textract')
    
    response = client.analyze_document(Document={'Bytes': image_binary},
        FeatureTypes=["TABLES", "FORMS"])
  
    
    #fetch detected blocks
    blocks=response['Blocks']
    width, height =image.size  
    
    #initialize parameters
    prevText = ''
    
    dicflag={};
    dicname = {};
    
    for i in range(1,6):
        i = str(i);
        dicflag.update({i:False});
        dicname.update({i:''});
   
   
   
    # Iterate over detected blocks and save data
    for block in blocks:
        #detect raw data and analyze using structure logic
        dataList, prevText,dicflag,dicname = DetectRCData(block,dataList,prevText,dicflag,dicname)
        
    #save detected Name to dataList
    dataList = updateName(dicname,dataList)
    
    return len(blocks),dataList


#save detected Name to dataList
def updateName(dicname,dataList):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]');
    for i in range(1,6):
        i = str(i)
        if(dicname[i] != '' and regex.search(dicname[i]) == None and ('and' in dicname[i]) == False ):
            dataList.update( {'Name' : dicname[i]} );
    
    return dataList
    
    
    
    
#Main Function
def main():
    fetchData();
   
    
if __name__ == "__main__":
    main()
