#python3
'''
This script retrieves all recognized image files in the current working directory
and renames these files according to their modified time.

Usage: python3 renameImagesByDateStamp.py [options]
Where options:
    -test       - perform a simulation of the operation and outputs a report
    -r          - recursive operation

'''

import os
import sys
import subprocess
from datetime import datetime

argv = sys.argv[1:]
argc = len( argv )

allowedExtensions = [ 'jpg', 'jpeg', 'png', 'bmp', 'gif' ]

def renameFile( oldName, newName ):
    if oldName == None or len( oldName ) == 0:
        raise ValueError( oldName )
    if newName == None or len( oldName ) == 0:
        raise ValueError( newName )
    if os.path.exists( newName ):
        raise FileExistsError( newName )

    if sys.platform.startswith( 'win32' ):
        cmd = [ 'move', oldName, newName ]
        #cmd = 'move "{}" "{}"'.format( oldName, newName )
    else:
        cmd = [ 'mv', oldName, newName ]
        #cmd = 'mv {} {}'.format(oldName, newName)

    try:
        subprocess.run( cmd, shell=True )
        #os.system( cmd )
    except FileNotFoundError as fnferror:
        print( 'File not found error on: {}'.format( cmd ) )
        raise
    except Exception as error:
        raise

def getImagesInDir( directory, outImageList, recursive = False ):
    subDirectories = []
    for path in os.listdir( directory ):
        path = os.path.join( directory, path )
        if os.path.isdir( path ):
            subDirectories.append( path )
            continue
        if not os.path.isfile( path ):
           print( 'ERROR > Not a file: {}'.format( path ) )
           continue
        isImage = False
        for ext in allowedExtensions:
            isImage = isImage or path.lower().endswith('.{}'.format(ext))
        if not isImage:
            continue
        outImageList.append( path )
    if recursive:
        for subDirectory in subDirectories:
            subPath = os.path.join( directory, subDirectory )
            getImagesInDir( subPath, outImageList, recursive )

def renameImagesInDir( imagesList, test = False ):
    testDuplicate = {}

    for imageFile in imagesList:
        modtime = datetime.utcfromtimestamp( os.path.getmtime( imageFile ) )
        #modtimeFmt = modtime.strftime( '%Y%m%d_%H%M%S_%f' )
        modtimeFmt = modtime.strftime('%Y%m%d_%H%M%S')
        splitted = os.path.splitext( imageFile )
        ext = splitted[1]
        directory = os.path.split( imageFile )[0]
        newFilename = ( modtimeFmt + ext )
        newPathAndFilename = os.path.join( directory, newFilename )

        if not newFilename in testDuplicate:
            testDuplicate[ newFilename ] = []

        if newFilename in testDuplicate:
            newSubFilename = '{}_{:03}{}'.format(
                modtimeFmt, len( testDuplicate[ newFilename ] ) + 1, ext )
            newPathAndFilename = os.path.join( directory, newSubFilename )
            testDuplicate[ newFilename ].append( newPathAndFilename )
            if not newSubFilename in testDuplicate:
                testDuplicate[ newSubFilename ] = []

        if test:
            print( '{} -> {}'.format( imageFile, newPathAndFilename ) )
            continue
        try:
            renameFile( imageFile, newPathAndFilename )
            print( '{} -> {}'.format( imageFile, newPathAndFilename ) )
        except Exception as error:
            print( error )
            raise

    if test:
        for file, where in testDuplicate.items():
            duplicateCount = len( where )
            if duplicateCount > 1:
                print( '{} has {} duplicates renamed to:'.format( file, duplicateCount ) )
                for newRenamed in where:
                    print( '\t{}'.format( newRenamed ) )

imageList = []

# gather all image files in current directory
getImagesInDir( os.getcwd(), imageList, '-r' in argv )
renameImagesInDir( imageList, '-test' in argv )

print( '\nDone.' )
sys.exit(0)