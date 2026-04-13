@echo off
echo ===============================
echo XPADI PROOF ENGINE BUILD
echo ===============================

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo Building executable...
pyinstaller --onefile --windowed ^
--name XPADI-Proof-Engine ^
app\main.py

echo Build complete!
pause