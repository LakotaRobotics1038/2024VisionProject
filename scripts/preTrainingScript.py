
import argparse
from pathlib import Path 
import os
import numpy as np
import cv2
import random 

# os.path.join(os.path.expanduser('~'), '

parser = argparse.ArgumentParser()
parser.add_argument(
    "--path-dir",
    dest = "path",
    type = Path,
    default= os.path.join(os.path.expanduser('~'), 'workspace', '2024VisionProject', 'mk1')
    )


parser.add_argument(
    "--data-dir",
    dest = "data",
    type = Path,
    default= os.path.join(os.path.expanduser('~'), 'workspace', '2024VisionProject','BetterData')
    )

args = parser.parse_args()

train = 0.6
validate = .375 #this is 15% of the whole but wee substract 60% adn tehn take teh next part so its 3/8 of the remaining
test = 0.25

jpgList = []
for each in os.listdir(args.data):
    if each.endswith(".jpg"):
        jpgList.append(each)

TrainData = random.sample(jpgList, k=int(len(jpgList)*train))
Train = open(os.path.join(args.path,"Train.txt"), "w")
for each in TrainData:
    imgPath = os.path.join(args.data, each)
    Train.write(imgPath + "\n")
Train.close()
    
jpgList = [x for x in jpgList if x not in TrainData]
#above line subtracts every element of TrainData from jpgList

ValidateData = random.sample(jpgList, k = int(len(jpgList)*validate))
Validate = open(os.path.join(args.path,"Validate.txt"), "w")
for each in ValidateData:
    imgPath = os.path.join(args.data, each)
    Validate.write(imgPath + "\n")
Validate.close()
    
TestData = [x for x in jpgList if x not in ValidateData]
Test  = open(os.path.join(args.path,"Test.txt"), "w")
for each in TestData:
    imgPath = os.path.join(args.data, each)
    Test.write(imgPath + "\n")
Test.close()

mk1 = open(os.path.join(args.path, "mk1.data"), "w")
mk1.write("train = " + os.path.join(args.path,"Train.txt") + "\n")
mk1.write("validate = " + os.path.join(args.path, "Validate.txt") + "\n")
mk1.write("test = " + os.path.join(args.path, "Test.txt") + "\n")
mk1.write("backup = " + os.path.join(args.path, "backup") + '\n')
mk1.write("names = " + os.path.join(args.path, 'ApLabels.txt'))
mk1.close()

print("done")
