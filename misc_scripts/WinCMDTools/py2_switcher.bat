%= opens command prompt, goes to (flash drive) directory and sets environment var =%
%= to make python 2.7 the default version of python. =%

@echo off

set "PATH=C:\Python27\;C:\Python27\scripts;%PATH%"

powershell

cd "C:\Users\James\Documents\_Github-Projects"