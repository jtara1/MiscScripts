%= opens command prompt, goes to (flash drive) directory and sets environment var =%
%= to make python 3.6 the default version of python. =%

@echo off

set "PATH=C:\Python36\;C:\Python36\scripts;%PATH%"

powershell

cd "C:\Users\James\Documents\_Github-Projects"