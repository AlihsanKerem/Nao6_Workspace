@echo off
set "CHORE_DIR=C:\Program Files (x86)\SoftBank Robotics\Choregraphe Suite 2.8"
set "PYTHONHOME=%CHORE_DIR%\lib\python2.7"
set "PYTHONPATH=%CHORE_DIR%\lib"
set "PATH=%CHORE_DIR%\bin;%CHORE_DIR%\lib;%PATH%"

"%CHORE_DIR%\bin\python.exe" %*
