#############################
# OS = Ubuntu 16 (Kubuntu 16)
# Desktop Environment = KDE
# Author = github.com/jtara1
# see README.md for more info
#############################

#### Personal Directories ####
mkdir ~/temp
mkdir ~/lib
mkdir ~/software

# path for containing github repositories or projects
GITHUB=~/_Github-Projects
mkdir $GITHUB

#### INSTALLING SOFTWARE & LIBRARIES ####
sudo apt update

# install git and download jtara1's collection of scripts and configurations
sudo apt install git -y
git clone https://github.com/jtara1/misc_scripts $GITHUB/misc_scripts
# root location for scripts & configs
MISC_SCRIPTS=$GITHUB/misc_scripts/misc_scripts

# install tilda (pull down absolute floating terminal-like program for bash)
sudo apt install tilda -y

# install simple screen recorder
#sudo add-apt-repository ppa:maarten-baert/simplescreenrecorder
#sudo apt update
#sudo apt install simplescreenrecorder
sudo apt install vokoscreen

# install open shot (video editor)
#sudo add-apt-repository ppa:openshot.developers/ppa
#sudo apt-get update
#sudo apt-get install openshot-qt

# install discord
#https://discordapp.com/api/download?platform=linux&format=deb
#sudo dpkg -i discord-0.0.4.deb
#sudo apt install -f

# install media info dll for usage with python module, get-media-info
sudo apt install python3-mediainfodll # 6.6 MiB

# install pip and virtualenv
sudo apt install python-pip python3-pip -y
sudo apt install python3-virtualenv -y

# install grub customizer
sudo add-apt-repository ppa:danielrichter2007/grub-customizer
sudo apt-get update
sudo apt-get install grub-customizer -y

# install chromium browser
sudo apt install chromium-browser -y

# python modules
sudo pip3 install youtube-dl
sudo pip3 install gallery-dl

# install do the right extraction
sudo apt install dtrx -y

# install curl
sudo apt install curl -y

# install npm 8.10.0 (node.js package manager)
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt install nodejs -y
sudo apt install build-essential -y

# install visudal studio code
#https://go.microsoft.com/fwlink/?LinkID=760868

# install brackets
#wget https://github.com/adobe/brackets/releases/download/release-1.12/Brackets.Release.1.12.64-bit.deb

# install atom
#https://atom.io/download/deb

# install JetBrains Toolbox
wget https://download.jetbrains.com/toolbox/jetbrains-toolbox-1.7.3593.tar.gz
dtrx jetbrains*
sudo mv jetbrains*/jetbrains-toolbox /bin/
rm jetbrains*

# install pycharm (python IDE)
echo "install pycharm-professional (needs license), pycharm-community, none [p/c/n]"
read answer
if [ "$answer" = "p" ]
then
    sudo snap install pycharm-professional
fi
elif [ "$answer" = "c" ]
then
    sudo snap install pycharm-community
fi

# install webstorm (javascript IDE)

#### CHANGE CONFIGURATIONS ####
# GRUB CUSTOMIZER:
# make windows loader default boot option
# change resolution in appearance settings to 1024x768x8

# SYSTEM SETTINGS
# use double click to open files
# enable num lock by default / on startup
# add custom global hotkey to open dolphin with Meta+E

# .bashrc
(cat .bashrc && cat $MISC_SCRIPTS/.bashrc) > jtara1-bashrc-temp
cat jtara1-bashrc-temp
echo "Copy text above to ~/.bashrc? [y/n]"
read answer
if [ "$answer" = "y" ]
then
    mv jtara1-bashrc-temp .bashrc
fi
rm jtara1-bashrc-temp

# CONFIG
cp $MISC_SCRIPTS/startup/linux-start.sh ~/.config/autostart-scripts
chmod +x ~/.config/autostart-scripts/linux-start.sh
# add ~/_Github-Projects/ and ~/Downloads/ and ~/Pictures/ to places in Dolphin

# copy blk-bg.html file to ~/Documents
cp $MISC_SCRIPTS/HTML/blk-bg.html ~/Documents

echo "use jtara1's hotkeys for KDE kwin, tilda, and more? [y/n]"
read answer
if [[ "$answer" = "" || "$answer" = "y" ]]
then
    # lower mouse acceleration to minimum value, 0.1
    cp $MISC_SCRIPTS/setup_ubuntu_environment/.kde/ ~/ -r
    # load KDE global hotkeys and application specific hotkeys or configurations
    cp $MISC_SCRIPTS/setup_ubuntu_environment/.config/ ~/ -r
fi

# install, start, and enable on startup, ksuperkey to bind Alt+F1 to Metakey (windows start key)
answer="y" # making this the default until someone doesn't want this
if [ "$answer" = "y" ]
then
    git clone https://github.com/hanschen/ksuperkey.git
    cd ksuperkey
    make
    sudo make install
    cd ..
    rm ksuperkey -r
    ksuperkey &
fi

# setup email and name used for github
echo "git setup:"
echo "global email: "
read email
echo "global name: "
read name

if [[ "$email" != "" && "$name" != "" ]]
then
    git config --global user.email "$email"
    git config --global user.name "$name"
fi

git config --global push.default simple

# update and upgrade packages
sudo apt update
sudo apt upgrade -y
