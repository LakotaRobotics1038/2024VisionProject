
import os


def makeTxtFiles():
    #this funtion creates .txt files for all images that don't contian a label
    path = # todo make relitive path

    os.remove("toDo path\train.txt")
    file = open("toDo path\train.txt")

    dirList = os.listdir(path)
    file.write("files and directories in "+path+":")

    for e in dirList:
        innerPath = path + "\\" + e
        innerList = os.listdir(innerPath)

        for item in innerList:
            file.write(f"{innerPath}{item}\n")

    file.close()

    makeTxtFiles()
