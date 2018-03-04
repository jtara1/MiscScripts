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

#### Install Software ####
sudo apt update

# install git and download jtara1's collection of scripts and configurations
sudo apt install git -y
git clone https://github.com/jtara1/misc_scripts $GITHUB/misc_scripts
# root location for scripts & configs
MISC_SCRIPTS=$GITHUB/misc_scripts/misc_scripts

# install tilda (pull down absolute floating terminal-like program for bash)
sudo apt install tilda -y

# install pip and virtualenv
sudo apt install python-pip python3-pip -y
sudo apt install python3-virtualenv -y

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
# enable num lock by default / on startup
# add custom global hotkey to open dolphin with Meta+E

# .bashrc
(cat .bashrc && cat $MISC_SCRIPTS/.bashrc) > jtara1-bashrc-temp
cat jtara1-bashrc-temp
echo "Save the text above to ~/.bashrc [y/n]"
read answer
if [ "$answer" = "y" ]
then
    mv jtara1-bashrc-temp .bashrc
fi
rm jtara1-bashrc-temp

# CONFIG
# move misc_scripts/misc_scripts/setup_ubuntu_enviornment/config/* to ~/.config/
# add ~/_Github-Projects/ and ~/Downloads/ and ~/Pictures/ to places in Dolphin

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
    ksuperkey
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
