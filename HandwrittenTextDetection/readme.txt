main.py  - if we give --train as command line argument(it will train the images of words)
           if we dont give any command line argument(it will detect words on images, then save all words as separate files in folder structure
           and then recognize the words and write to text file
           Saving detected words in files is to train them before there recognition so we can comment that line if we dont want to train them
   	
Functions
   -  DetectRecognizeImage  - Detect Textin the image and recognize them using already trained model
        -  cordinatesDetect  -  detect cordinates of rectangle drawn around the detected words
        -  sortCordinates  - sort cordinates based on there relative position in the image file
        -  setWordsBasedonCordinates  - recognize words using trained model
        -  writeToTextFile - write words to text file based on the sorted cordinates



text_detection.py - detect words based on East Detector Model
Model.py - train the model based on input images
DataLoader.py - load input files from directory structure to train them 


python main.py --train     ->    train input files
python main.py --validate   -> validate
python main.py       ->  detect and recognize words from input file and write text to sub-0.txt file