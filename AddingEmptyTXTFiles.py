
import os


def makeTxtFiles():
    
    #this funtion creates .txt files for all images that don't contian a label

    
    path = os.path.join("..","2024VisionProject","aprilTags","pictures")
    for folder in os.listdir(path):
        folderPath = os.path.join(path, folder)
        for imgList in os.listdir(folderPath):
            isThere = False
            if imgList.endswith(".jpg"):
                tempFileName = imgList.replace(".jpg", ".txt")
                for newImgList in os.listdir(folderPath):
                    if newImgList == tempFileName:
                        isThere = True
                if isThere == False:
                    filePath = os.path.join(folderPath, tempFileName)
                    newTXTFile = open(filePath, "a")
                    print(filePath)
                    newTXTFile.close()

makeTxtFiles()


















"""#os.remove(path)
    file = (path)

    dirList = os.listdir(path)
    file.write("files and directories in "+path+":")

    for e in dirList:
        innerPath = path + "\\" + e
        innerList = os.listdir(innerPath)

        for item in innerList:
            file.write("{innerPath}{item}\\n")

    Name = fileName
    tempName = fileName - ".jpg"
    for each in dirList:
        if tempName == tempName + ".txt":
            #something that makes this move on
            return 
        else:
            open(tempName.txt, x)
    file.close()

    makeTxtFiles()"""
   
