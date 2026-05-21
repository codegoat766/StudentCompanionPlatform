@echo off
setlocal

cd /d "%~dp0"

echo [1/3] Building executable with PyInstaller...
python -m PyInstaller --clean --noconfirm PRN_spa.spec
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo [2/3] Copying executable to project root...
copy /Y ".\dist\PRN_spa.exe" ".\PRN_spa.exe" >nul
if errorlevel 1 (
  echo Could not copy PRN_spa.exe to project root.
  exit /b 1
)

echo [3/3] Done.
echo Output:
echo   .\PRN_spa.exe
echo   .\dist\PRN_spa.exe

exit /b 0
