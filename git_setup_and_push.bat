@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================================
echo       HUONG DAN VA CONG CU DAY CODE LEN GITHUB
echo ========================================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] May tinh cua ban chua co Git!
    echo 1. Vui long tai va cai dat Git tai: https://git-scm.com/
    echo 2. Khi cai dat, giu nguyen cac tuy chon mac dinh.
    echo 3. Sau khi cai dat xong, mo lai file nay.
    echo.
    pause
    exit /b 1
)

echo [Buoc 1] Kiem tra kho Git local...
if not exist ".git" (
    echo Khoi tao kho Git moi...
    git init
    git branch -M main
    echo [OK] Da khoi tao Git branch 'main'.
) else (
    echo [OK] Kho Git local da ton tai.
)

echo.
echo [Buoc 2] Kiem tra ket noi Remote Repository (GitHub)...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Chua co dia chi Remote GitHub.
    echo Hay tao 1 Repository moi tren https://github.com/new (chon Public hoac Private, KHONG tich khoi tao README).
    echo Sau do copy link Repository (vi du: https://github.com/ten_ban/game_test_3d.git)
    echo.
    set /p REPO_URL="Dan link GitHub repository vao day: "
    if not "!REPO_URL!"=="" (
        git remote add origin !REPO_URL!
        echo [OK] Da gan remote origin: !REPO_URL!
    ) else (
        echo [CANH BAO] Ban chua nhap link Remote. Khong the day code len GitHub.
        pause
        exit /b 1
    )
) else (
    for /f "delims=" %%i in ('git remote get-url origin') do set CURRENT_REMOTE=%%i
    echo Remote hien tai: !CURRENT_REMOTE!
    echo (Neu muon doi link remote khac, hay go: git remote set-url origin [LINK_MOI])
)

echo.
echo [Buoc 3] Chon tat ca file de commit (git add)...
git add .
echo [OK] Da them cac file thay doi vao danh sach commit.

echo.
echo [Buoc 4] Tao Commit...
set /p COMMIT_MSG="Nhap thong diep commit (Bam Enter de dung mac dinh: 'Cap nhat game nong trai'): "
if "!COMMIT_MSG!"=="" set COMMIT_MSG=Cap nhat game nong trai

git commit -m "!COMMIT_MSG!"

echo.
echo [Buoc 5] Day code len GitHub (git push)...
git push -u origin main
if errorlevel 1 (
    echo.
    echo [THONG BAO] Push len 'main' gap van de, thu lai voi nhanh 'master'...
    git push -u origin master
)

if errorlevel 1 (
    echo.
    echo ========================================================
    echo [CANH BAO] Push len GitHub chua thanh cong!
    echo Co the do:
    echo 1. Ban chua dang nhap GitHub tren may (se co popup GitHub hien ra de Login).
    echo 2. Repo tren GitHub da co san file README (hay go: git pull origin main --rebase roi push lai).
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo [THANH CONG] Toan bo ma nguon va file cap nhat da duoc day len GitHub!
    echo ========================================================
)

echo.
pause
exit /b 0
