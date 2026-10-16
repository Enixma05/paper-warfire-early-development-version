@echo off
title Setup Environment - Proyek Gaming

echo ==========================================
echo   SETUP ENVIRONMENT PROYEK GAMING
echo ==========================================
echo.

cd /d "%~dp0"

set CONDA_CMD=

REM 1. Cek apakah conda ada di PATH
where conda >nul 2>&1
if not errorlevel 1 (
    set CONDA_CMD=conda
    goto :found_conda
)

REM 2. Deteksi lokasi instalasi standar Miniconda / Anaconda di Windows
if exist "%USERPROFILE%\miniconda3\condabin\conda.bat" (
    set CONDA_CMD=%USERPROFILE%\miniconda3\condabin\conda.bat
    goto :found_conda
)
if exist "%USERPROFILE%\anaconda3\condabin\conda.bat" (
    set CONDA_CMD=%USERPROFILE%\anaconda3\condabin\conda.bat
    goto :found_conda
)
if exist "%LOCALAPPDATA%\miniconda3\condabin\conda.bat" (
    set CONDA_CMD=%LOCALAPPDATA%\miniconda3\condabin\conda.bat
    goto :found_conda
)
if exist "%LOCALAPPDATA%\anaconda3\condabin\conda.bat" (
    set CONDA_CMD=%LOCALAPPDATA%\anaconda3\condabin\conda.bat
    goto :found_conda
)
if exist "C:\ProgramData\miniconda3\condabin\conda.bat" (
    set CONDA_CMD=C:\ProgramData\miniconda3\condabin\conda.bat
    goto :found_conda
)
if exist "C:\ProgramData\anaconda3\condabin\conda.bat" (
    set CONDA_CMD=C:\ProgramData\anaconda3\condabin\conda.bat
    goto :found_conda
)
if exist "C:\miniconda3\condabin\conda.bat" (
    set CONDA_CMD=C:\miniconda3\condabin\conda.bat
    goto :found_conda
)
if exist "C:\anaconda3\condabin\conda.bat" (
    set CONDA_CMD=C:\anaconda3\condabin\conda.bat
    goto :found_conda
)

echo [ERROR] Conda tidak ditemukan di sistem Anda.
echo.
echo Kemungkinan penyebab:
echo 1. Miniconda atau Anaconda belum diinstal.
echo    Download installer di: https://docs.conda.io/en/latest/miniconda.html
echo 2. Conda dipasang di lokasi custom.
echo.
echo SOLUSI:
echo Jalankan file ini melalui 'Anaconda Prompt' atau 'Miniconda Prompt' dari Start Menu Windows.
echo.
pause
exit /b 1

:found_conda
echo [INFO] Conda terdeteksi di: %CONDA_CMD%
echo.

REM Periksa apakah environment proyek-gaming sudah ada
"%CONDA_CMD%" env list | findstr /C:"proyek-gaming" >nul
if errorlevel 1 (
    echo [INFO] Membuat environment baru: proyek-gaming dengan Python 3.12
    "%CONDA_CMD%" create -n proyek-gaming python=3.12 pip -y
    if errorlevel 1 goto :error
) else (
    echo [INFO] Environment proyek-gaming sudah tersedia.
)

echo.
echo [INFO] Memasang atau memperbarui dependensi pytest, pyyaml, pygame
"%CONDA_CMD%" run -n proyek-gaming python -m pip install pytest pyyaml pygame
if errorlevel 1 goto :error

echo.
echo [INFO] Memperbarui requirements.txt
"%CONDA_CMD%" run -n proyek-gaming python -m pip freeze > requirements.txt
if errorlevel 1 goto :error

echo.
echo ==========================================
echo   SETUP SELESAI DAN BERHASIL!
echo ==========================================
echo Environment : proyek-gaming
echo Dependensi  : pytest, pyyaml, pygame
echo File        : requirements.txt
echo.
echo Rekan tim Anda sekarang sudah siap menjalankan kode proyek!
echo.
pause
exit /b 0

:error
echo.
echo [ERROR] Terjadi kegagalan saat proses setup.
pause
exit /b 1
