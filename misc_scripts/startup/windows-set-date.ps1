#!C:\WINDOWS\system32\ powershell.exe
# requires admin
# sets the date to 8 hours ago
# fixes a problem I have when booting into windows after linux

set-date (get-date).AddHours(-7)
