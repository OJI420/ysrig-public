@echo off
setlocal

set SCRIPT_NAME=_ysrig_installer_setup.py

echo Searching for the latest installed Maya version...

set LATEST_MAYA_PATH=
set LATEST_MAYA_DIR_NAME=
for /d %%d in ("C:\Program Files\Autodesk\Maya*") do (
    if exist "%%d\bin\mayapy.exe" (
        set LATEST_MAYA_PATH=%%d
        set LATEST_MAYA_DIR_NAME=%%~nd
    )
)

if not defined LATEST_MAYA_PATH (
    echo ERROR: Could not find any Maya installation.
    pause
    exit /b
)

rem "Maya2025" から "Maya" を取り除いて "2025" を取得
set MAYA_VERSION=%LATEST_MAYA_DIR_NAME:Maya=%

echo Latest version found: %MAYA_VERSION%

set MAYAPY_EXE="%LATEST_MAYA_PATH%\bin\mayapy.exe"
set SCRIPT_FULL_PATH="%~dp0%SCRIPT_NAME%"

echo.
echo Executing script...
echo.

rem 実行
%MAYAPY_EXE% %SCRIPT_FULL_PATH% %MAYA_VERSION%

endlocal