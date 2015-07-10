import os
import time
import subprocess
import sys
 
fileList = []
rootdir = raw_input("Root Dir: ")
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
    print "Removing %s" % inFile
    os.remove(inFile)

print 'Reached EOF'
