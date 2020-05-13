#!C:\WINDOWS\system32\ powershell.exe
# requires admin
# sets the date to 8 hours ago
# fixes a problem I have when booting into windows after linux

# Win10 will re-open ps over and over if I quick launch the source script as an executable so run this instead

Start-Process "$psHome\powershell.exe" -verb runas -ArgumentList "-file C:\Users\James\Desktop\windows-set-date.ps1"
