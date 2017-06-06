#!/usr/bin/env python3
import sys

def main(arguments):
    #outputPath = arguments[0]
    geneTableFilePath = "output.table"
    filesToUse = getFilesWithExtension(arguments[0:],'excov')
    table = makePAVTable(filesToUse)
    createTableFile(geneTableFilePath,table)

def getFilesWithExtension(arguments,extension):
    filesWithExtension = []
    for argument in arguments:
        argumentFile = argument.split('/')[-1]
        argumentExtension = argumentFile.split(".")[1:]
        if extension in argumentExtension:
            filesWithExtension.append(argument)
    return filesWithExtension

def makePAVTable(files):
    totalPAVs = {}
    tablePAVs = {}
    allGenes = []

    for item in files:
        openFile = open(item,"r")
        PAV = PAVForFile(openFile)
        totalPAVs[openFile.name.split("/")[-1]] = PAV
        for sortItem in PAV:
            genesToAdd = PAV[sortItem]
            for geneToAdd in genesToAdd:
                if geneToAdd not in allGenes:
                    allGenes.append(geneToAdd)
        openFile.close()
    
    for PAVname in totalPAVs:
        PAVGenes = {}
        PAV = totalPAVs[PAVname]

        presentGenes = PAV['PRESENT']
        lostGenes = PAV['LOST']
        errorGenes = PAV['ERROR']
        
        for gene in allGenes:
            if gene in presentGenes:
                PAVGenes[gene] = 1
            elif gene in lostGenes:
                PAVGenes[gene] = 0
            elif gene in errorGenes:
                PAVGenes[gene] = 2
            else:
                PAVGenes[gene] = 0
        
        totalPAVs[PAVname] = PAVGenes
    return totalPAVs

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

def createTableFile(outputFilePath,table):
    oldTable = []
    readingFile = open(outputFilePath,"r")
    presentGenes = readingFile.readline().replace("\n","").split(",")
    if(presentGenes == [""]):
        presentGenes =['variationName']
    for line in readingFile:
        oldTable.append(line.replace("\n",""))
    readingFile.close()

    for variation in table:
        variationLine = ""
        variationLineList = [0] * len(presentGenes)
        variationLineList[0] = variation
        PAV = table[variation]
        for gene in PAV:
            genesToAdd = []
            print(gene)
            if gene in presentGenes:
                geneIndex = presentGenes.index(gene)
                print(geneIndex)
                print(PAV[gene])
                variationLineList[geneIndex] = PAV[gene]
                print(variationLineList)
            else:
                genesToAdd.append(gene)
                presentGenes.append(gene)
                variationLineList.append(PAV[gene])
                print(gene)
        variationLine = listToCsv(variationLineList)
        oldTable.append(variationLine)

    print(presentGenes)
    geneHeader = listToCsv(presentGenes) + listToCsv(genesToAdd) + "\n"
    print(geneHeader)
    outputFile = open(outputFilePath,'w')
    outputFile.write(geneHeader)
    for line in oldTable:
        outputFile.write(line+"\n")
    outputFile.close()

def listToCsv(listToParse):
    output = ""
    for item in listToParse:
        output += str(item)+","
    return output[:-1]

main(sys.argv[1:])
