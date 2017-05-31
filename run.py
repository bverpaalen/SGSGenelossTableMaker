#!/usr/bin/env python3
import sys

def main(arguments):
    outputFile = newOutputFile('PAV.table')
    filesToUse = getFilesWithExtension(arguments,'excov')
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
        openFile.close()

def openFileForRead(itemToRead):
    return open(itemToRead,'r')

def newOutputFile(fileName):
    return open(fileName,'w')

main(sys.argv[1:])
