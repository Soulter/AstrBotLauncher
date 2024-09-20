@echo off
chcp 936 >nul
setlocal

:: Clear screen and output Banner
cls
echo.
echo =========================
echo    AstrBot Launcher v0.1.0
echo =========================
echo.

set PYTHON_CMD=python

:: Check if Python is installed
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.9 or higher.
    goto end
)

:: Get Python version
for /f "tokens=2 delims= " %%a in ('%PYTHON_CMD% --version 2^>^&1') do (
    set PYTHON_VERSION=%%a
)

:: Extract major and minor version numbers
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

:: Check if Python version is less than 3.9
if %PYTHON_MAJOR% lss 3 (
    echo [ERROR] Python 3.9 or higher is required. Current version is %PYTHON_VERSION%.
    goto end
)

if %PYTHON_MAJOR%==3 if %PYTHON_MINOR% lss 9 (
    echo [ERROR] Python 3.9 or higher is required. Current version is %PYTHON_VERSION%.
    goto end
)

:: Python version meets the requirement
echo [INFO] Python version meets the requirement. Current version is %PYTHON_VERSION%.
echo.

:: Check if AstrBot or QQChannelChatGPT folder exists
if not exist AstrBot (
    if not exist QQChannelChatGPT (
        echo [INFO] AstrBot or QQChannelChatGPT folder not found. Downloading the latest version from GitHub...
        call :downloadLatestRelease
        goto end
    )
)

echo [INFO] AstrBot or QQChannelChatGPT folder already exists. No need to download.
echo.
goto RunAstrBot

:downloadLatestRelease
:: Call GitHub API to get the latest release information
powershell -Command "$release = Invoke-WebRequest -Uri 'https://api.github.com/repos/Soulter/AstrBot/releases/latest' -ErrorAction Stop | ConvertFrom-Json; echo $release.zipball_url" > latest.txt

:: Check if the download URL was successfully obtained
if not exist latest.txt (
    echo [ERROR] Failed to obtain the latest version information.
    goto end
)

:: Read the download link from latest.txt
set /p download_url=<latest.txt

echo [INFO] Downloading the latest version of AstrBot from %download_url%...

:download
:: Download the latest zipball version
powershell -Command "Invoke-WebRequest -Uri '%download_url%' -OutFile 'latest.zip'"

:: Check if the download was successful
if not exist latest.zip (
    echo [ERROR] Failed to download the latest version file. You can manually download the zip from https://github.com/Soulter/AstrBot/releases/latest, then extract the **folder inside the zip** to the current directory and rename it to AstrBot.
    goto end
)

:: Clear screen
cls
echo [INFO] The file has been downloaded to latest.zip.

:: Extract the latest version files
echo [INFO] Extracting the latest version files...
echo.
powershell -Command "Expand-Archive -Path 'latest.zip' -DestinationPath '.' -Force"

:: Check if the extraction was successful
if errorlevel 1 (
    echo [ERROR] An error occurred while extracting the latest version files. You can manually download the zip from https://github.com/Soulter/AstrBot/releases/latest, then extract the **folder inside the zip** to the current directory and rename it to AstrBot.
    goto end
)

:: Rename the extracted folder to AstrBot
for /d %%I in ("Soulter-AstrBot-*") do (
    if exist "%%I" (
        ren "%%I" AstrBot
    )
)

echo.
echo [INFO] AstrBot download is complete.
echo.

:: Delete the downloaded zip file and latest.txt
del latest.zip
del latest.txt

:RunAstrBot
:: Change to AstrBot or QQChannelChatGPT directory and run main.py
cd AstrBot || cd QQChannelChatGPT
echo [INFO] Checking for dependency updates.
echo.
%PYTHON_CMD% -m pip install -r requirements.txt

echo [INFO] Starting AstrBot.
echo.
%PYTHON_CMD% main.py

cd ..

:end
endlocal
pause