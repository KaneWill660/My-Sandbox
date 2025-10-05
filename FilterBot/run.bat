@echo off
chcp 65001 >nul
echo ========================================
echo    Telegram Flow Bot - Filter Messages
echo ========================================
echo.
echo Dang khoi dong bot...
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Loi: Python chua duoc cai dat!
    echo Vui long cai dat Python 3.7+ tu https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Kiem tra file config
if not exist "config.json" (
    echo Loi: Khong tim thay file config.json!
    echo Vui long tao file config.json theo huong dan trong README.md
    pause
    exit /b 1
)

REM Cai dat thu vien neu can
echo Dang kiem tra va cai dat thu vien...
pip install -r requirements.txt

REM Chay bot
echo.
echo Bot da san sang! Nhan Ctrl+C de dung.
echo.
python run_utf8.py

pause
