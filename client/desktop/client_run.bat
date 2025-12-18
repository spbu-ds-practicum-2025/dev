@echo off

pip install -r requirements.txt

IF ERRORLEVEL 1 (
    echo Install error.
    pause
    exit /b 1
)

echo ---------------------
echo     System Launch
echo ---------------------

python main.py

pause
