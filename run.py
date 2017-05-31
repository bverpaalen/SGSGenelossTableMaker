#!/usr/bin/env python3
import sys

def main(arguments):
    filesToUse = getFilesWithExtension(arguments,'excov')
    

def getFilesWithExtension(arguments,extension):
    filesWithExtension = []
    for argument in arguments:
        argumentFile = argument.split('/')[-1]
        argumentExtension = argumentFile.split(".")[1:]
        if extension in argumentExtension:
            filesWithExtension.append(argument)
    return filesWithExtension

main(sys.argv[1:])
