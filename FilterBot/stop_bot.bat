@echo off
chcp 65001 >nul
echo ========================================
echo    Stopping Telegram Flow Bot
echo ========================================
echo.

REM Tim va dung process Python dang chay bot
echo Dang tim va dung bot...
taskkill /f /im python.exe >nul 2>&1
if errorlevel 1 (
    echo Khong tim thay process Python nao dang chay
) else (
    echo Da dung tat ca process Python
)

echo.
echo Bot da duoc dung!
echo.
pause
