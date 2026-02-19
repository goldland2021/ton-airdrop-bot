@echo off
chcp 65001 > nul
echo ========================================
echo TON空投仪表盘Bot - 重启脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖包...
pip list | findstr "pyTelegramBotAPI" > nul
if errorlevel 1 (
    echo 安装依赖包...
    pip install pyTelegramBotAPI requests
)

REM 停止现有Bot进程
echo 停止现有Bot进程...
taskkill /F /IM python.exe /T > nul 2>&1
timeout /t 2 /nobreak > nul

REM 启动Bot
echo 启动TON空投Bot...
cd /d "%~dp0"
python run_bot.py

echo.
echo ========================================
echo Bot已启动！按Ctrl+C停止
echo ========================================
pause