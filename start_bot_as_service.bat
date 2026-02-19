@echo off
chcp 65001 > nul
echo ========================================
echo TON空投仪表盘Bot - 服务模式启动
echo ========================================
echo.
echo 此脚本将Bot设置为后台服务模式运行
echo 即使关闭命令行窗口，Bot也会继续运行
echo.

REM 检查Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python
    pause
    exit /b 1
)

REM 安装必要工具（如果未安装）
echo 检查必要工具...
where nssm > nul 2>&1
if errorlevel 1 (
    echo 下载NSSM（Non-Sucking Service Manager）...
    powershell -Command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'"
    powershell -Command "Expand-Archive -Path 'nssm.zip' -DestinationPath 'nssm' -Force"
    copy "nssm\win64\nssm.exe" .\ > nul 2>&1
    rd /s /q nssm > nul 2>&1
    del nssm.zip > nul 2>&1
)

REM 创建服务
echo 创建Windows服务...
nssm install TONAirdropBot "C:\Windows\py.exe" "run_bot.py"
nssm set TONAirdropBot AppDirectory "%~dp0"
nssm set TONAirdropBot Description "TON空投仪表盘Telegram Bot服务"
nssm set TONAirdropBot Start SERVICE_AUTO_START
nssm set TONAirdropBot AppStdout "%~dp0\bot_service.log"
nssm set TONAirdropBot AppStderr "%~dp0\bot_service_error.log"

echo.
echo 服务创建完成！
echo.
echo 可用命令：
echo   启动服务：net start TONAirdropBot
echo   停止服务：net stop TONAirdropBot
echo   删除服务：nssm remove TONAirdropBot confirm
echo.
echo 查看日志：查看 bot_service.log 文件
echo.

REM 询问是否立即启动
set /p start_now="是否立即启动服务？(y/n): "
if /i "%start_now%"=="y" (
    echo 启动服务...
    net start TONAirdropBot
    echo 服务已启动！
)

pause