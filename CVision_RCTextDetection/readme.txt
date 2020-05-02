------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
APPROACH

I have used AWS Textract API Model(Access Key and Secret Access Key setup required for access AWS API) to detect words from RC Image. 
Detected words were raw data from Image and needs to be recognized as required Information
I have applied logic to detect raw words and identified them and saved to Excel File(named as FinalRCData.xlsx)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

MODULES USED

 - boto3(AWS Textract)
 - OpenCV(Image Processing)
 - glob(File Handling)
 - dateutil(Date Handling)
 - PIL(Image Handling)
 - Pandas(DataFrame Handling)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Program is taking Image files from RC folder, so for Input we need to put Images in RC folder and as output It will Save fetched Data in FinalRCData.xlsx file.
For some Images, there is no Registration and Manufacturing Date mentioned and hence, we will get N/A as value for those fields.
For few Images, there are no Licence number, Chasis number and Engine Number and hence, we will get N/A as value for those fields.
For few cases, if detected word is not fitting the logic due to wrong detection, it will show N/A value for them as well.

I have saved my output file as RCData to show my output data.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

RUN

COMMAND ->  python TextDetect.py

INPUT -> Save Input Images in RC folder to test(If they will be in JPG format, it will change them to PNG format and remove JPG files.

OUTPUT -> FinalRCData.xlsx

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

