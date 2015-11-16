#!/bin/bash
# Script Name: Media Installer
# Author: Jacob Carrigan
# Publisher: https://www.github.com/carrigan98
#

# DO NOT EDIT ANYTHING UNLESS YOU KNOW WHAT YOU ARE DOING.
SCRIPTPATH=$(pwd)
APPVERSION="1.9.6"

function pause(){
   read -p "$*"
}

clear
echo

echo -e '--->FileBot installation will start soon. Please read the following carefully.'

echo -n 'Type the username of the user you want to run FileBot as and press [ENTER]. Typically, this is your system login name (IMPORTANT! Ensure correct spelling and case): '
read UNAME

if [ ! -d "/home/$UNAME" ] || [ -z "$UNAME" ]; then
	echo -e 'Bummer! You may not have entered your username correctly. Exiting now. Please rerun script.'
	echo
	pause 'Press [Enter] key to continue...'
	cd $SCRIPTPATH
	exit 0
fi
UGROUP=($(id -gn $UNAME))

echo

echo -e '--->Refreshing packages list...'
sudo apt-get update

echo
sleep 1

echo -e '--->Installing prerequisites...'
sudo apt-get -y install openjdk-8-jre-headless

echo
sleep 1

echo -e '--->Downloading latest FileBot...'
sudo mkdir -p /tmp/filebot
cd /tmp/filebot
sudo wget -O filebot-amd64.deb 'http://filebot.sourceforge.net/download.php?type=deb&arch=amd64'

echo
sleep 1

echo -e '--->Configuring FileBot Install...'
sudo dpkg --force-depends -i filebot-*.deb
sudo apt-get -f install

echo
sleep 1

echo -e '--->Removing temporary FileBot Files...'
sudo rm -rf /tmp/filebot

echo
sleep 1

echo -e '--->FileBot Install Complete.'
echo

pause 'Press [Enter] key to continue...'

cd $SCRIPTPATH
sudo ./setup.sh
exit 0
