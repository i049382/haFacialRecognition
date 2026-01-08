@echo off
REM Sync integration files to Home Assistant (Windows batch version)

set SOURCE_DIR=integration
set TARGET_DIR=ha_config\custom_components\face_recognition

echo === Syncing Face Recognition Integration ===
echo Source: %SOURCE_DIR%
echo Target: %TARGET_DIR%
echo.

REM Check if target directory exists
if not exist "%TARGET_DIR%" (
    echo ❌ Target directory not found: %TARGET_DIR%
    echo    Make sure ha_config symbolic link is working
    pause
    exit /b 1
)

echo Files to sync:
dir /b "%SOURCE_DIR%\*.py" "%SOURCE_DIR%\*.yaml" "%SOURCE_DIR%\*.json" 2>nul

echo.
echo Copying files...

REM Copy Python files
for %%f in ("%SOURCE_DIR%\*.py") do (
    if exist "%%f" (
        copy "%%f" "%TARGET_DIR%\" >nul
        echo ✅ %%~nxf
    )
)

REM Copy YAML files
for %%f in ("%SOURCE_DIR%\*.yaml") do (
    if exist "%%f" (
        copy "%%f" "%TARGET_DIR%\" >nul
        echo ✅ %%~nxf
    )
)

REM Copy JSON files
for %%f in ("%SOURCE_DIR%\*.json") do (
    if exist "%%f" (
        copy "%%f" "%TARGET_DIR%\" >nul
        echo ✅ %%~nxf
    )
)

echo.
echo === Sync Complete ===
echo.
echo Next steps:
echo 1. Restart Home Assistant
echo 2. Test the integration
echo.
echo To restart HA:
echo   - Go to Settings → System → RESTART
echo   - Or use: ha core restart ^(if SSH available^)
pause