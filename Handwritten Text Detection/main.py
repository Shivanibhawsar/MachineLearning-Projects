from __future__ import division
from __future__ import print_function

from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
from PIL import Image
import cv2
import editdistance
from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess
import os
import collections
import tensorflow as tf
tf.reset_default_graph()


class FilePaths:
	"filenames and paths to data"
	fnCharList = 'model/charList.txt'
	fnAccuracy = 'model/accuracy.txt'
	fnTrain = 'data/'
	fnInfer = 'data/test.png'
	fnCorpus = 'data/corpus.txt'


def train(model, loader):
    
	"train NN"
    
	epoch = 0 # number of training epochs since start
	bestCharErrorRate = float('inf') # best valdiation character error rate
	noImprovementSince = 0 # number of epochs no improvement of character error rate occured
	earlyStopping = 5 # stop training after this number of epochs without improvement
	while True:
		epoch += 1
		print('Epoch:', epoch)

		# train
		print('Train NN')
		loader.trainSet()
		while loader.hasNext():
			iterInfo = loader.getIteratorInfo()
			batch = loader.getNext()
			loss = model.trainBatch(batch)
			print('Batch:', iterInfo[0],'/', iterInfo[1], 'Loss:', loss)

		# validate
		charErrorRate = validate(model, loader)
		
		# if best validation accuracy so far, save model parameters
		if charErrorRate < bestCharErrorRate:
			print('Character error rate improved, save model')
			bestCharErrorRate = charErrorRate
			noImprovementSince = 0
			model.save()
			open(FilePaths.fnAccuracy, 'w').write('Validation character error rate of saved model: %f%%' % (charErrorRate*100.0))
		else:
			print('Character error rate not improved')
			noImprovementSince += 1

		# stop training if no more improvement in the last x epochs
		if noImprovementSince >= earlyStopping:
			print('No more improvement since %d epochs. Training stopped.' % earlyStopping)
			break


def validate(model, loader):
	"validate NN"
	print('Validate NN')
	loader.validationSet()
	numCharErr = 0
	numCharTotal = 0
	numWordOK = 0
	numWordTotal = 0
	while loader.hasNext():
		iterInfo = loader.getIteratorInfo()
		print('Batch:', iterInfo[0],'/', iterInfo[1])
		batch = loader.getNext()
		(recognized, _) = model.inferBatch(batch)
		
		print('Ground truth -> Recognized')	
		for i in range(len(recognized)):
			numWordOK += 1 if batch.gtTexts[i] == recognized[i] else 0
			numWordTotal += 1
			dist = editdistance.eval(recognized[i], batch.gtTexts[i])
			numCharErr += dist
			numCharTotal += len(batch.gtTexts[i])
			print('[OK]' if dist==0 else '[ERR:%d]' % dist,'"' + batch.gtTexts[i] + '"', '->', '"' + recognized[i] + '"')
	
	# print validation result
	charErrorRate = numCharErr / numCharTotal
	wordAccuracy = numWordOK / numWordTotal
	print('Character error rate: %f%%. Word accuracy: %f%%.' % (charErrorRate*100.0, wordAccuracy*100.0))
	return charErrorRate


def infer(model, fnImg):
	"recognize text in image provided by file path"
	img = "real_and_recon.png"
	
	#cv2.imshow("hh",img)
	img = preprocess(cv2.imread(img, cv2.IMREAD_GRAYSCALE), Model.imgSize)
	batch = Batch(None, [img])
	(recognized, probability) = model.inferBatch(batch, True)
	print(recognized)
	#print('Probability:', probability[0])
	return recognized;


def DetectRecognizeImage(decoderType,dump):
        
        for itr in range(1):
                
                #fileName = 'Buffalo_Dataset/' + 'AARsummary_' + str(itr) + '_1' + '.png';
                fileName = 'dataset/N3.png'
                print(fileName)
                image = cv2.imread(fileName)
                orig = image.copy()
                
                (H, W) = image.shape[:2]
                (newW, newH) = (320,320)
                rW = W / float(newW)
                rH = H / float(newH)
                image = cv2.resize(image, (newW, newH))
                (H, W) = image.shape[:2]
                layerNames = [
                "feature_fusion/Conv_7/Sigmoid",
                "feature_fusion/concat_3"]
                print("[INFO] loading EAST text detector...")
                net = cv2.dnn.readNet('frozen_east_text_detection.pb')
                blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                (123.68, 116.78, 103.94), swapRB=True, crop=False)
                start = time.time()
                net.setInput(blob)
                (scores, geometry) = net.forward(layerNames)
                end = time.time()
                (numRows, numCols) = scores.shape[2:4]
                rects = []
                confidences = []
                for y in range(0, numRows):
                # extract the scores (probabilities), followed by the geometrical
                # data used to derive potential bounding box coordinates that
                    # surround text
                        scoresData = scores[0, 0, y]
                        xData0 = geometry[0, 0, y]
                        xData1 = geometry[0, 1, y]
                        xData2 = geometry[0, 2, y]
                        xData3 = geometry[0, 3, y]
                        anglesData = geometry[0, 4, y]

                        # loop over the number of columns
                        for x in range(0, numCols):
                                # if our score does not have sufficient probability, ignore it
                                if scoresData[x] < 0.5:
                                        continue

                                # compute the offset factor as our resulting feature maps will
                                # be 4x smaller than the input image
                                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                                # extract the rotation angle for the prediction and then
                                # compute the sin and cosine
                                angle = anglesData[x]
                                cos = np.cos(angle)
                                sin = np.sin(angle)

                                # use the geometry volume to derive the width and height of
                                # the bounding box
                                h = xData0[x] + xData2[x]
                                w = xData1[x] + xData3[x]

                                # compute both the starting and ending (x, y)-coordinates for
                                # the text prediction bounding box
                                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                                startX = int(endX - w)
                                startY = int(endY - h)

                                # add the bounding box coordinates and probability score to
                                # our respective lists
                                rects.append((startX, startY, endX, endY))
                                confidences.append(scoresData[x])

                # apply non-maxima suppression to suppress weak, overlapping bounding
                # boxes
                boxes = non_max_suppression(np.array(rects), probs=confidences)
                
                cordinates,pageWords = cordinatesDetect(boxes,rW,rH,orig);
                model = Model(open(FilePaths.fnCharList).read(), decoderType, mustRestore=True, dump=False)
                cordinates,box_to_display_str_map = setWordsBasedonCordinates(itr,pageWords,model,cordinates)
                cordinates , newlinelist = sortCordinates(cordinates)
                writeToTextFile(itr,cordinates,box_to_display_str_map,newlinelist)
                        
                
                        
def cordinatesDetect(boxes,rW,rH,orig):
        
        pageWords = []
        cordinates=[]
        
                
        for (startX, startY, endX, endY) in boxes:
                                    # scale the bounding box coordinates based on the respective
                                # ratios
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)
                # draw the bounding box on the image
                cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
                #cv2.imshow("Text Detection2", orig)
                        
                cordinates.append([startX, startY])
                roi = orig[startY:endY, startX:endX]
                pageWords.append(roi)
        return cordinates,pageWords

def sortCordinates(cordinates):
        ctr = 0;
        print(cordinates)
        
        cordinates = sorted(cordinates , key=lambda k: [k[1]])
        group = []
        newlinelist = []
        finallist = []
        reference = cordinates[0][1]
        print("reference")
        print(reference)
        for c in cordinates:
                
                diff = c[1] - reference
                reference = c[1]
                print(diff)
                if(diff >= 10):
                        
                        group = sorted(group , key=lambda k: [k[0]])
                        newlinelist.append(group[0])
                        finallist.extend(group)
                        group = []
                        group.append(c)
                else:
                        group.append(c);
        group = sorted(group , key=lambda k: [k[0]])
        newlinelist.append(group[0])
        finallist.extend(group)
                        
        print("After")
        print(finallist)
        print(newlinelist)
        return finallist , newlinelist





             
def setWordsBasedonCordinates(itr,pageWords,model,cordinates):
        ctr = 0;
        if not os.path.exists('sub'):
                os.makedirs('sub');
        if not os.path.exists('sub/sub-sub-'+str(itr)):
                os.makedirs('sub/sub-sub-'+ str(itr))
        box_to_display_str_map = collections.defaultdict(list)
                    

        pagewordlist = []
        for imgitr in pageWords:
                print(open(FilePaths.fnAccuracy).read())
                print("HELLO")
                        
                Image.fromarray(imgitr.astype(np.uint8)).save("real_and_recon.png")
                image1 = cv2.imread("real_and_recon.png")
                #cv2.imwrite('sub/sub-sub-'+str(itr)+ '/' + 'sub-sub-%d.png'%ctr, image1)
                recogword = infer(model, image1);
                #print (cordinates[ctr])
                box = tuple(cordinates[ctr])
                ctr = ctr + 1;
                
                box_to_display_str_map.update( {box : recogword} )
                pagewordlist.append(recogword)
        
        return cordinates , box_to_display_str_map


def writeToTextFile(itr,cordinates,box_to_display_str_map,newlinelist):
        filewrite = open('sub-'+str(itr)+'.txt','w')
                #print(box_to_display_str_map)
        newlineptr = 1
        maxnewline = len(newlinelist)
        print("newline")
        
        for pg in cordinates:
                      #print(pg.getNext())
                
                
                if( pg in newlinelist):
                        filewrite.write('\n')
                        print("newlinehi")
                pg = tuple(pg)
                newlineptr = newlineptr+1
                filewrite.write(box_to_display_str_map[pg].pop())
                filewrite.write(" ")
                
        filewrite.close()
    


def main():
	"main function"
	# optional command line args
	parser = argparse.ArgumentParser()
    
	parser.add_argument('--train', help='train the NN', action='store_true')
	parser.add_argument('--validate', help='validate the NN', action='store_true')
	parser.add_argument('--beamsearch', help='use beam search instead of best path decoding', action='store_true')
	parser.add_argument('--wordbeamsearch', help='use word beam search instead of best path decoding', action='store_true')
	parser.add_argument('--dump', help='dump output of NN to CSV file(s)', action='store_true')

	args = parser.parse_args()

	decoderType = DecoderType.BestPath
	if args.beamsearch:
		decoderType = DecoderType.BeamSearch
	elif args.wordbeamsearch:
		decoderType = DecoderType.WordBeamSearch

	# train or validate on IAM dataset	
	if args.train or args.validate:
		# load training data, create TF model
		loader = DataLoader(FilePaths.fnTrain, Model.batchSize, Model.imgSize, Model.maxTextLen)

		# save characters of model for inference mode
		open(FilePaths.fnCharList, 'w').write(str().join(loader.charList))
		
		# save words contained in dataset into file
		open(FilePaths.fnCorpus, 'w').write(str(' ').join(loader.trainWords + loader.validationWords))

		# execute training or validation
		if args.train:
			model = Model(loader.charList, decoderType)
			train(model, loader)
		elif args.validate:
			model = Model(loader.charList, decoderType, mustRestore=True)
			validate(model, loader)

	# infer text on test image
	else:
		print(open(FilePaths.fnAccuracy).read())
		DetectRecognizeImage(decoderType, args.dump)
        


if __name__ == '__main__':
	main()

