@echo off
echo Dang dong bot cu...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Dang khoi dong bot moi...
cd /d "E:\MySandbox\SummayBot"
python telegram_coin_tracker_bot.py

pause
