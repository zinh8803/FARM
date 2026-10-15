@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================================
echo        CAP NHAT GAME NONG TRAI VIET (GIT PULL)
echo ========================================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Git tren he thong.
    echo Vui long cai dat Git tai: https://git-scm.com/
    pause
    exit /b 1
)

echo [1/3] Dang kiem tra ket noi den Git repository...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo [CANH BAO] Thu muc nay chua duoc lien ket voi Git remote repository.
    echo Hay chay file 'git_setup_and_push.bat' de thiet lap truoc.
    pause
    exit /b 1
)

echo [2/3] Dang dong bo commit moi nhat tu remote (git fetch)...
git fetch origin

echo [3/3] Dang keo ma nguon moi nhat ve may (git pull)...
git pull origin main
if errorlevel 1 (
    echo [THONG BAO] Khong the pull tu nhanh 'main', dang thu lai voi nhanh 'master'...
    git pull origin master
)

if errorlevel 1 (
    echo.
    echo [CANH BAO] Co the ban co cac thay doi chua commit gay xung dot.
    echo Hay kiem tra lai 'git status'.
) else (
    echo.
    echo [THANH CONG] Game da duoc cap nhat len phien ban moi nhat tu Git!
)

echo.
echo ========================================================
echo Nhan phim bat ky de thoat...
echo ========================================================
pause >nul
exit /b 0
