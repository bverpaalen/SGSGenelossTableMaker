#!/usr/bin/env python3
import sys

def main(arguments):
    #outputPath = arguments[0]
    geneTableFilePath = "output.table"
    geneTableFile = appendRWFile(geneTableFilePath)
    filesToUse = getFilesWithExtension(arguments[0:],'excov')
    tabel = makePAVTable(filesToUse,geneTableFile)
    geneTableFile.close()

def getFilesWithExtension(arguments,extension):
    filesWithExtension = []
    for argument in arguments:
        argumentFile = argument.split('/')[-1]
        argumentExtension = argumentFile.split(".")[1:]
        if extension in argumentExtension:
            filesWithExtension.append(argument)
    return filesWithExtension

def makePAVTable(files,geneTableFile):
    totalPAVs = {}
    allGenes = []

    for item in files:
        openFile = openFileForRead(item)
        PAV = PAVForFile(openFile)
        totalPAVs[openFile.name.split("/")[-1]] = PAV
        for sortItem in PAV:
            genesToAdd = PAV[sortItem]
            for geneToAdd in genesToAdd:
                if geneToAdd not in allGenes:
                    allGenes.append(geneToAdd)
        openFile.close()

    for PAVname in totalPAVs:
        PAV = totalPAVs[PAVname]
        presentGenes = PAV['PRESENT']
        lostGenes = PAV['LOST']
        errorGenes = PAV['ERROR']

def openFileForRead(itemToRead):
    return open(itemToRead,'r')

def appendRWFile(fileName):
    return open(fileName,'a+')

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
