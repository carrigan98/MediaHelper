import os
import time
import subprocess
import sys
import argparse
 
parser = argparse.ArgumentParser(description="File conversion script")
parser.add_argument('-i','--input',help='The root source that will be converted')
parser.add_argument('-nd','--nodelete',help='Do not delete file after conversion')
 
args = vars(parser.parse_args())
delete = True
fileList = []

if (args['input']):
	rootdir = (str(args['input']))
else:
	rootdir = raw_input("Root Dir: ")
	
if (args['nodelete']):
	delete = False

for root, subFolders, files in os.walk(rootdir):
    for file in files:
        theFile = os.path.join(root,file)
        fileName, fileExtension = os.path.splitext(theFile)
        if fileExtension.lower() in ('.avi', '.divx', '.flv', '.m4v', '.mkv', '.mov', '.mpg', '.mpeg', '.wmv'):
            print "Adding %s" % theFile
            fileList.append(theFile)

while fileList:
    inFile = fileList.pop()
    fileName, fileExtension = os.path.splitext(inFile)
    outFile = fileName+'.mp4'
 
    print "Processing %s" % inFile

    command = 'HandBrakeCLI -i "{0}" -o "{1}" --preset="AppleTV 3"'.format(
        inFile,
        outFile
    )

    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    )
    (results, errors) = proc.communicate()

    if proc.returncode is not 0:
        print '"HandBrakeCLI (compress) returned status code: %d" % proc.returncode'

    time.sleep(5)
    if delete:
		if os.path.isfile(outFile):
			print "Removing %s" % inFile
			os.remove(inFile)

print 'Reached EOF'
