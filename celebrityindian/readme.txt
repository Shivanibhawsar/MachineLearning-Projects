Crawl popular websites & create a database of Indian movie celebrities with their images and personality traits.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

domain - in.bookmyshow.com
start_urls = ['https://in.bookmyshow.com/entertainment/movies/hindi/']

Crawling Celebrities webpages to fetch their personality in database along with their images

---------------------------------------------------------------------------------------------------------------------------
PRE-REQUISITE -> run below command in MySQL to create table for saving data

create database Celebrity;
use Celebrity;
create table CelebrityDetail(
id int primary key,
Name varchar(100),
Picture LONGBLOB,
Personality varchar(1000)
);
Above table should be empty before running this code
----------------------------------------------------------------------------------------------------------------------------

RUN COMMAND in CMD-
scrapy crawl celebrity


RUN WITHOUT LOGS in CMD-
scrapy crawl --nolog celebrity


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ITEM_PIPELINES must need to be set

CLOSESPIDER_PAGECOUNT are set to 155 for crawling 155 pages. We can further extend it to crawl remaning pages as well

We are filtering sub domain links of bookmyshow for celebrity pages and ignoring movies detail page

Fetched data is present in data folder in JSON format as well as excel fetched from Database
IndianCelebrity Database.sql file is exported from MYSQL Database and can be viewed in MySQL

