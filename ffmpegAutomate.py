#!/usr/bin/python3

'''
ffmpegAutomate
Automates certain fixed operations on a list of files.

mp4tomkv - converts .mp4 files into .mkv files
small - creates a smaller version of the file sacrificing some quality.
'''

import os

class ffmpegAutomate:
    DEFAULT_FILE_CONVERT = 'convertfiles.txt'
    DEFAULT_FILE_SMALLIFY = 'smallifyfiles.txt'

    def __init__( self ):
        self.cwd = os.getcwd()
        self.appBinFolder = os.path.join( self.cwd, 'bin' )
        self.operations = {
            'mp4tomkv' : {
                'cmd' : 'ffmpeg_mp4_to_mkv.cmd',
                'msg' : 'mp4 to mkv conversion',
                'substr' : '',
                },
            'small' : {
                'cmd' : 'ffmpeg_small.cmd',
                'msg' : 'smallify',
                'substr' : 'small',
                }
            }

        self.filesToConvert = []
        self.filesToSmallify = []
        self.start()

    def start( self ):
        fileConvertSource = os.path.join( self.cwd, ffmpegAutomate.DEFAULT_FILE_CONVERT )
        if os.path.exists( fileConvertSource ) and os.path.isfile( fileConvertSource ):
            with open( fileConvertSource, 'r' ) as outWriter:
                for line in outWriter:
                    line = str( line ).strip()
                    if line != None and len( line ) > 0:
                        self.filesToConvert.append( line )

        fileSmallifySource = os.path.join( self.cwd, ffmpegAutomate.DEFAULT_FILE_SMALLIFY )
        if os.path.exists( fileSmallifySource ) and os.path.isfile( fileSmallifySource ):
            with open( fileSmallifySource, 'r' ) as outWriter:
                for line in outWriter:
                    line = str( line ).strip()
                    if line != None and len(line) > 0:
                        self.filesToSmallify.append( line )

        self.performOpOnList( 'mp4tomkv', self.filesToConvert )
        self.performOpOnList( 'small', self.filesToSmallify )

    def performOpOnList( self, operation, list ):
        if operation is None or ( operation not in self.operations ):
            print( 'Operation: {} is not valid.'.format( operation ) )
            return

        if list is None:
            print( 'List is invalid.' )
            return

        op = self.operations[ operation ]
        command = os.path.join( self.appBinFolder, op[ 'cmd' ] )

        if not os.path.exists( command ) or not os.path.isfile( command ):
            print( 'Command: {} is not found!'.format( command ) )
            return

        if len( list ) > 0:
            print( '>>> START BATCH OPERATION: {}'.format( op[ 'msg' ] ) )
            for file in list:
                if not os.path.exists( file ) or not os.path.isfile( file ):
                    print( 'File: {} does not exist or is not a file. Skipping...'.format( file ) )
                    continue
                fileName, fileExt = os.path.splitext( file )
                fileTarget = fileName
                if len( op[ 'substr' ] ) > 0:
                    fileTarget = fileTarget + '.' + op[ 'substr' ]
                fileTarget = fileTarget + fileExt
                print( 'Performing {} of file: {} to file: {}'.format(
                    op[ 'msg' ],
                    str( file ),
                    str( fileTarget )
                    ) )
                commandLine = command + ' "' + file + '" "' + fileTarget + '"'
                try:
                    os.system( commandLine )
                except Exception as error:
                    print( 'Error while executing command line: {}\nError: {}'.format(
                        commandLine,
                        str( error )
                        ) )
                    continue
            print( '>>> END BATCH OPERATION: {}'.format( op[ 'msg' ] ) )


# command line
if __name__ == '__main__':
    ffmpegAutomate().start()