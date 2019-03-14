import os
import time
import subprocess
import sys
import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(filename=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'encodeLog.log'))
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# create a parser for arguments
parser = argparse.ArgumentParser(description="File conversion script")
parser.add_argument('-i','--input',help='The root source that will be converted')
parser.add_argument('-nd','--nodelete',help='Do not delete file after conversion')
 
args = vars(parser.parse_args())
delete = True
fileList = []

# create a pid file
pid=str(os.getpid())
pidfile=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'encodeDir.pid')

if os.path.isfile(pidfile):
	print "%s already exists, exiting" % pidfile
	sys.exit()
file(pidfile, 'w').write(pid)
try:

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
				logger.info('Adding %s', theFile)
				fileList.append(theFile)

	while fileList:
		inFile = fileList.pop()
		fileName, fileExtension = os.path.splitext(inFile)
		outFile = fileName+'.mp4'
	 
		logger.info('Processing %s', inFile)

		command = 'HandBrakeCLI -i "{0}" -o "{1}" --preset="AppleTV 3" --optimize --subtitle "1,2,3,4,5,6,7,8,9,10"'.format(
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
			logger.error('HandBrakeCLI (compress) returned status code: %d', proc.returncode)

		time.sleep(5)
		if delete:
			if os.path.isfile(outFile):
				logger.info('Removing %s', inFile)
				os.remove(inFile)

	logger.info('Reached EOF')
finally:
	os.unlink(pidfile)
