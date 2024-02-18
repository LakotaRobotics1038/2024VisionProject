
#import argparse as args
import os
import numpy as np
import cv2
import random 

Path = "/home/jetson/workspace/2024VisionProject/mk1"
DataPath = "/home/jetson/workspace/2024VisionProject/BetterData"

#Train = open( Path + "/Train.txt", "w")
#Validate = open(Path + "/Validate.txt", "w")
#Test  = open(Path + "/Test.txt", "w")

Train = 0.6
Validate = 0.15
Test = 0.25

jpgList = []
for each in os.listdir(DataPath):
    if each.endswith(".jpg"):
        jpgList.append(each)
print(jpgList)
