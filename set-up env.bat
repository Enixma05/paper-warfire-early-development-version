
@echo off
setlocal
title Setup Environment - Proyek Gaming

echo ==========================================
echo   SETUP ENVIRONMENT PROYEK GAMING
echo ==========================================
echo.

REM Masuk ke folder tempat file BAT berada
cd /d "%~dp0"

REM Periksa apakah Conda tersedia
where conda >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Conda tidak ditemukan di PATH.
    echo Jalankan file ini melalui Anaconda Prompt
    echo atau Miniconda Prompt.
    pause
    exit /b 1
)

REM Periksa apakah environment sudah tersedia
call conda env list | findstr /B /C:"proyek-gaming " >nul
if errorlevel 1 (
    echo [INFO] Membuat environment proyek-gaming...
    call conda create -n proyek-gaming python=3.12 pip -y
    if errorlevel 1 goto :error
) else (
    echo [INFO] Environment proyek-gaming sudah ada.
)

REM Aktifkan environment
call conda activate proyek-gaming
if errorlevel 1 goto :error

echo.
echo [INFO] Python yang digunakan:
python --version
if errorlevel 1 goto :error

echo.
echo [INFO] Memasang dependensi...
python -m pip install pytest pyyaml pygame
if errorlevel 1 goto :error

echo.
echo [INFO] Membuat requirements.txt...
python -m pip freeze > requirements.txt
if errorlevel 1 goto :error

echo.
echo ==========================================
echo   SETUP SELESAI
echo ==========================================
echo Environment : proyek-gaming
echo Folder      : %CD%
echo Dependensi  : requirements.txt
echo.
echo Isi requirements.txt:
type requirements.txt
echo.
pause
exit /b 0

:error
echo.
echo [ERROR] Setup gagal. Periksa pesan di atas.
pause
exit /b 1
