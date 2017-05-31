#!/usr/bin/env python3
import sys

def main(arguments):
    outputPath = arguments[0]
    outputFile = newOutputFile(outputPath)
    filesToUse = getFilesWithExtension(arguments[1:],'excov')
    tabel = makePAVTable(filesToUse)
    outputFile.close()

def getFilesWithExtension(arguments,extension):
    filesWithExtension = []
    for argument in arguments:
        argumentFile = argument.split('/')[-1]
        argumentExtension = argumentFile.split(".")[1:]
        if extension in argumentExtension:
            filesWithExtension.append(argument)
    return filesWithExtension

def makePAVTable(files):
    for item in files:
        openFile = openFileForRead(item)
        PAV = PAVForFile(openFile)
        for item in PAV:
            print(item+": "+str(PAV[item]))
        openFile.close()

def openFileForRead(itemToRead):
    return open(itemToRead,'r')

def newOutputFile(fileName):
    return open(fileName,'w')

def PAVForFile(readFile):
    presentGenes = []
    absentGenes = []
    errorGenes = []
    headerLine = readFile.readline().replace("\n","")
    headers = headerLine.split(",")
    geneIdIndex = headers.index("ID")
    isLostIndex = headers.index("is_lost")

    for line in readFile:
        content = line.split(",")
        contentIsLost = content[isLostIndex]
        contentId = content[geneIdIndex]
        if contentIsLost == "PRESENT":
            presentGenes.append(contentId)
        elif contentIsLost == "LOST":
            absentGenes.append(contentId)
        else:
            errorGenes.append(contentId)
    result = {"PRESENT":presentGenes,"LOST":absentGenes,"ERROR":errorGenes}
    return result

main(sys.argv[1:])
