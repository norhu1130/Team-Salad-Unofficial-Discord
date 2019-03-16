@echo off

:main
title Please Wait...
chcp 65001
color 0b
title Run Team Salad Bot
goto menu

:menu
cls
echo.
echo 1. Module Insatll OR Update (Must run as administrator)
echo 2. Run Team Salad Bot (Must run as nomal)
echo 3. Exit
echo.
set /p b=Input a number and press Enter. : 
if %b% == 1 goto Module_Install
if %b% == 2 goto Run
if %b% == 3 goto out

:out
cls
exit

:Module_Install
cls
bcdedit > nul || (echo you must run this file as an administrator & pause & goto menu)
echo If you have Python 3.6, press Enter.
pause
cls
python -m pip install --upgrade pip
python -m pip install discord
python -m pip install datetime
python -m pip install PyNaCl
python -m pip install youtube_dl
pyhton -m pip install beautifulsoup4
python -m pip install requests
python -m pip install oauth2
python -m pip install pymysql
echo.
echo ==============================
echo Press Enter to return to Main.
echo ==============================
echo.
pause
goto menu

:Run
cls
echo ==============================
echo Please Wait...
echo ==============================
echo.
bcdedit > nul || (echo Bot is booting! & echo. & python salad.py & pause)
echo you must not run this file as an administrator
echo Please run this fill as nomal
echo.
pause
echo.
echo ==============================
echo Press Enter to return to Main.
echo ==============================
echo.
pause
goto menu