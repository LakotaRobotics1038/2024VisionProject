
import argparse as args
from pathlib import Path 
import os
import numpy as np
import cv2
import random 

#Path = "/home/jetson/workspace/2024VisionProject/mk1"
#DataPath = "/home/jetson/workspace/2024VisionProject/BetterData"
def __init__:
    parser = argparse.AgrumentParser()
    parser.addArgument(
        "--path-dir",
        type = Path,
        default= Path(__file__).absolute().parent / "path",
        help= os.path.join("home", "jetson","workspace","2024VisionProject","mk1"))

    parser = argparse.ArgumentParser()
    parser.addArgument(
        "--data-dir",
        type = Path,
        default= Path(__file__).absolute().parent / "data",
        help= os.path.join("home", "jetson","workspace","2024VisionProject","mk1"))
        

train = 0.6
validate = .375 #this is 15% of the whole but wee substract 60% adn tehn take teh next part so its 3/8 of the remaining
test = 0.25

jpgList = []
for each in os.listdir(DataPath):
    if each.endswith(".jpg"):
        jpgList.append(each)

TrainData = random.sample(jpgList, k=int(len(jpgList)*train))
Train = open(os.path.join(Path,"Train.txt"), "w")
for each in TrainData:
    imgPath = os.path.join(DataPath, each)
    Train.write(imgPath + "\n")
Train.close()
    
jpgList = [x for x in jpgList if x not in TrainData]
#above line subtracts every element of TrainData from jpgList

ValidateData = random.sample(jpgList, k = int(len(jpgList)*validate))
Validate = open(os.path.join(Path,"Validate.txt"), "w")
for each in ValidateData:
    imgPath = os.path.join(DataPath, each)
    Validate.write(imgPath + "\n")
Validate.close()
    
TestData = [x for x in jpgList if x not in ValidateData]
Test  = open(os.path.join(Path,"Test.txt"), "w")
for each in TestData:
    imgPath = os.path.join(DataPath, each)
    Test.write(imgPath + "\n")
Test.close()

mk1 = open(Path + "/mk1.data", "w")
mk1.write("train = " + Path + "/Train.txt" + "\n")
mk1.write("validate = " + Path + "/Validate.txt" + "\n")
mk1.write("test = " + Path + "/Test.txt" + "\n")
mk1.write("backup = " + Path + "/backup")
mk1.close()

print("done")
