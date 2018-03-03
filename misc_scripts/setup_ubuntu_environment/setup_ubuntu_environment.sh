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

#### Install Software ####
sudo apt update

# install git
sudo apt install git -y

# install tilda (absolute floating terminal-like program for bash)
sudo apt install tilda -y

# install grub customizer
sudo add-apt-repository ppa:danielrichter2007/grub-customizer
sudo apt-get update
sudo apt-get install grub-customizer -y

# install chromium browser
sudo apt install chromium-browser -y

#### Change Configurations ####
# GRUB CUSTOMIZER:
# make windows loader default boot option
# change resolution in appearance settings to 1024x768x8

# SYSTEM SETTINGS
# use double click to open files
# change mouse pointer acceleration to 0.1
# enable num lock by default / on startup
# add custom global hotkey to open dolphin with Meta+E

# CONFIG
# move misc_scripts/misc_scripts/setup_ubuntu_enviornment/config/* to ~/.config/
echo "use jtara1's hotkeys for KDE kwin, tilda, and more? [y/n]"
read answer
if [[ "$answer" = "" || "$answer" = "y" ]]
then
    cd ~/temp
    git clone https://github.com/jtara1/misc_scripts
    cp misc_scripts/misc_scripts/setup_ubuntu_environment/config/* ~/.config -r
    rm misc_scripts -rf
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
    ksuperkey
fi

# setup dev environment
mkdir ~/_Github-Projects

# setup email and name used for github
echo "github setup:"
echo "global email: "
read email
echo "global name: "
read name

if [[ "$email" != "" && "$name" != "" ]]
then
    git config --global user.email "$email"
    git config --global user.name "$name"
fi
