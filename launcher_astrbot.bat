@echo off
chcp 65001 >nul
setlocal

:: 清屏并输出 Banner
cls
echo.
echo =========================
echo    AstrBot Launcher v0.1.0
echo =========================
echo.

set PYTHON_CMD=python


:: 检查是否安装了 Python
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Python 未安装，请安装 Python 3.9 或更高版本。
    goto end
)

:: 获取 Python 版本
for /f "tokens=2 delims= " %%a in ('%PYTHON_CMD% --version 2^>^&1') do (
    set PYTHON_VERSION=%%a
)

:: 提取主版本号和次版本号
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

:: 检查 Python 版本是否小于 3.9
if %PYTHON_MAJOR% lss 3 (
    echo [错误] 需要 Python 3.9 或更高版本，当前版本为 %PYTHON_VERSION%。
    goto end
)

if %PYTHON_MAJOR%==3 if %PYTHON_MINOR% lss 9 (
    echo [错误] 需要 Python 3.9 或更高版本，当前版本为 %PYTHON_VERSION%。
    goto end
)

:: Python 版本符合要求
echo [信息] Python 版本符合要求，当前版本为 %PYTHON_VERSION%。
echo.

:: 检查当前目录是否存在 AstrBot 或 QQChannelChatGPT 文件夹
if not exist AstrBot (
    if not exist QQChannelChatGPT (
        echo [信息] 未找到 AstrBot 或 QQChannelChatGPT 文件夹，将从 GitHub 下载最新版本...
        call :downloadLatestRelease
        goto end
    )
)

echo [信息] AstrBot 或 QQChannelChatGPT 文件夹已存在，无需下载。
echo.
goto RunAstrBot

:downloadLatestRelease
:: 调用 GitHub API 获取最新发布版本信息
powershell -Command "$release = Invoke-WebRequest -Uri 'https://api.github.com/repos/Soulter/AstrBot/releases/latest' -ErrorAction Stop | ConvertFrom-Json; echo $release.zipball_url" > latest.txt

:: 检查是否成功获取下载 URL
if not exist latest.txt (
    echo [错误] 无法获取最新版本信息。
    goto end
)

:: 从 latest.txt 中读取下载链接
set /p download_url=<latest.txt

echo [信息] 正在从 %download_url% 下载最新的 AstrBot 版本...

:download
:: 下载最新版本 zipball
powershell -Command "Invoke-WebRequest -Uri '%download_url%' -OutFile 'latest.zip'"

:: 检查是否下载成功
if not exist latest.zip (
    echo [错误] 无法下载最新版本文件。你可以手动前往 https://github.com/Soulter/AstrBot/releases/latest 下载压缩包，然后将 **压缩包中的文件夹** 解压到当前目录，重命名为 AstrBot。
    goto end
)

:: 清屏
cls
echo [信息] 文件已经下载到 latest.zip。

:: 解压最新版本文件
echo [信息] 正在解压最新版本文件...
echo.
powershell -Command "Expand-Archive -Path 'latest.zip' -DestinationPath '.' -Force"

:: 检查是否解压成功
if errorlevel 1 (
    echo [错误] 解压最新版本文件时发生错误。你可以手动前往 https://github.com/Soulter/AstrBot/releases/latest 下载压缩包，然后将 **压缩包中的文件夹** 解压到当前目录，重命名为 AstrBot。
    goto end
)

:: 重命名解压后的文件夹为 AstrBot
for /d %%I in ("Soulter-AstrBot-*") do (
    if exist "%%I" (
        ren "%%I" AstrBot
    )
)

echo.
echo [信息] 下载 AstrBot 操作完成。
echo.

:: 删除下载的 zip 文件和 latest.txt
del latest.zip
del latest.txt

:RunAstrBot
:: 切换到 AstrBot 或 QQChannelChatGPT 目录并执行 main.py
cd AstrBot || cd QQChannelChatGPT
echo [信息] 正在启动 AstrBot.
echo.
%PYTHON_CMD% main.py

cd ..


:end
endlocal
pause
