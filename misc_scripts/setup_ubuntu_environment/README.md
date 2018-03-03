# setup_ubuntu_environment

This installs the software that I use and optionally configures hotkeys and settings.

My personal hotkeys changed or added:

KDE global hotkeys [kwin]
| Name | Hotkey |
| --- | --- |
| tile left | Meta+left |
| tile right | Meta+right |
| maximize | Meta+up |
| minimize | Meta+down |
| close window | Alt+x |
| show all windows | Alt+a |
| open system menu | Meta |

Tilda and Konsole hotkeys (Konsole hotkeys are default, tilda's changed to conform)
| Name | Hotkey |
| --- | --- |
| go to next tab | Shift+right |
| go to previous tab | Shift+left |
| move tab right | Ctrl+Shift+right |
| move tab left | Ctrl+Shift+left |

## Requirements
OS = Ubuntu 16 (Kubuntu 16)
Desktop Environment = KDE

## Download files
```
wget --no-check-certificate --content-disposition https://github.com/jtara1/misc_scripts/archive/master.zip
unzip misc_scripts-master.zip
cd misc_scripts-master/misc_scripts/setup_ubuntu_environment
```

## Usage
```
chmod +x setup_ubuntu_environment.sh
./setup_ubuntu_environment.sh
```