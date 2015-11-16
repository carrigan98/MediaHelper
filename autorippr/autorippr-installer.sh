#!/bin/bash
# Script Name: Media Installer
# Author: Jacob Carrigan
# Publisher: https://www.github.com/carrigan98
#

# DO NOT EDIT ANYTHING UNLESS YOU KNOW WHAT YOU ARE DOING.
SCRIPTPATH=$(pwd)

function pause(){
   read -p "$*"
}

clear
echo

echo -e '--->Autorippr installation will start soon. Please read the following carefully.'

echo -n 'Type the username of the user you want to run Autorippr as and press [ENTER]. Typically, this is your system login name (IMPORTANT! Ensure correct spelling and case): '
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
sudo apt-get -y install \
    git-core \
    python-dev \
    python-pip \
    handbrake-cli
python -c "import setuptools"
if [ $? != 0 ]; then
    sudo mkdir -p /tmp/ez-setup
    cd /tmp/ez-setup
    sudo wget https://bootstrap.pypa.io/ez_setup.py 
    sudo python ez_setup.py
    python -c "import setuptools"
    if [ $? != 0 ]; then
        echo -e "Install of setuptools Failed."
        echo
        pause 'Press [Enter] key to continue...'
        cd $SCRIPTPATH
        sudo ./setup.sh
        exit 0
    fi
    sudo rm -rf /tmp/ez-setup
fi
cd $SCRIPTPATH
sudo pip install tendo pyyaml peewee

if [ ! -e "/usr/bin/makemkvcon" ]; then
    cd $SCRIPTPATH
    echo -e '--->Installing MakeMKV...'
    sudo ./makemkv-installer.sh
fi

if [ ! -e "/usr/bin/filebot" ]; then
    cd $SCRIPTPATH
    echo -e '--->Installing FileBot...'
    sudo ./filebot-installer.sh
fi

echo
sleep 1

echo -e '--->Downloading latest Autorippr...'
cd /home/$UNAME
git clone https://github.com/JasonMillward/Autorippr /home/$UNAME/autoMR || { echo -e 'Git not found.' ; exit 1; }

echo
sleep 1

echo -e "--->Copying settings file and setting permissions..."
sudo cp $SCRIPTPATH/autorippr-settings.cfg /home/$UNAME/autoMR/settings.cfg || { echo -e 'Initial settings move failed.' ; exit 1; }
sudo chown -R $UNAME:$UGROUP /home/$UNAME/autoMR >/dev/null 2>&1
sudo chmod 775 -R /home/$UNAME/autoMR >/dev/null 2>&1

echo 
sleep 1

echo -e '--->Autorippr Install Complete.'
echo

pause 'Press [Enter] key to continue...'

cd $SCRIPTPATH
sudo ./setup.sh
exit 0
