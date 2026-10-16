@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================================
echo     EXPORT GAME NONG TRAI VIET - XUAT BAN GAME
echo ========================================================
echo.

:: === Tim Godot ===
set "GODOT_EXE="

for %%f in ("%~dp0godot*.exe" "%~dp0..\godot*.exe") do (
    if exist "%%~f" (
        set "GODOT_EXE=%%~f"
        goto :found_godot
    )
)

if exist "%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe" (
    set "GODOT_EXE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe"
    goto :found_godot
)
if exist "%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe" (
    set "GODOT_EXE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe"
    goto :found_godot
)
if exist "%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" (
    set "GODOT_EXE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe"
    goto :found_godot
)

if exist "%USERPROFILE%\Downloads\" (
    for /r "%USERPROFILE%\Downloads" %%f in (Godot*win64*.exe) do (
        if exist "%%~f" (
            set "GODOT_EXE=%%~f"
            goto :found_godot
        )
    )
)

where godot >nul 2>&1
if not errorlevel 1 (
    set "GODOT_EXE=godot"
    goto :found_godot
)

echo [LOI] Khong tim thay Godot! Hay dat Godot vao thu muc game hoac Downloads.
pause
exit /b 1

:found_godot
echo [OK] Tim thay Godot: "!GODOT_EXE!"
echo.

if not exist "%~dp0project.godot" (
    echo [LOI] Khong tim thay project.godot trong thu muc: %~dp0
    pause
    exit /b 1
)

:: === Buoc 1: Import project (headless) ===
echo [1/4] Dang import project (can thiet truoc khi export)...
"!GODOT_EXE!" --headless --editor --quit
if errorlevel 1 (
    echo [LOI] Godot import project that bai. Xem loi Godot phia tren.
    pause
    exit /b 1
)
echo [OK] Import hoan tat.
echo.

:: === Buoc 2: Export game ===
set "EXPORT_NAME=LittleDaNang.exe"
echo [2/4] Dang export game ra file: %EXPORT_NAME% ...

"!GODOT_EXE!" --headless --export-release "Windows Desktop" "%~dp0%EXPORT_NAME%"

if not exist "%~dp0%EXPORT_NAME%" (
    echo [LOI] Export that bai! Kiem tra lai export preset trong Godot Editor.
    echo      Mo Godot Editor ^> Project ^> Export ^> Tao preset "Windows Desktop"
    echo.
    echo [THU LAI] Dang thu export voi debug mode...
    "!GODOT_EXE!" --headless --export-debug "Windows Desktop" "%~dp0%EXPORT_NAME%"
)

if not exist "%~dp0%EXPORT_NAME%" (
    echo [LOI] Van khong the export! Hay mo Godot Editor va export thu cong.
    pause
    exit /b 1
)

echo [OK] Da export thanh cong: %EXPORT_NAME%
echo.

:: === Buoc 3: Tao GitHub Release de nguoi choi tai cap nhat ===
echo [3/3] Ban co muon dang ban export len GitHub Releases khong?
echo       Nguoi choi co the bam Cap nhat trong game, khong can Git/.git.
echo.
set /p DO_RELEASE="Nhap Y de tao release, hoac Enter de bo qua: "

if /i not "!DO_RELEASE!"=="Y" goto :done

where gh >nul 2>&1
if errorlevel 1 (
    echo [LOI] Can cai GitHub CLI (gh) va dang nhap bang: gh auth login
    goto :done
)

for /f "usebackq delims=" %%v in (`powershell -NoProfile -Command "(Get-Content '%~dp0version.json' -Raw | ConvertFrom-Json).version"`) do set "VERSION=%%v"
if not defined VERSION (
    echo [LOI] Khong doc duoc version trong version.json.
    goto :done
)
set "TAG=v!VERSION!"
echo Tao PCK, patch SHA-256 va release !TAG!...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0publish_patch.ps1" -GodotExe "!GODOT_EXE!" -GameExe "%~dp0%EXPORT_NAME%" -Version "!VERSION!" -Repository "zinh8803/FARM"
if errorlevel 1 (
    echo [LOI] Khong the tao patch/manifest hoac tai release len GitHub.
) else (
    echo [OK] Da tai exe, PCK baseline, patch va update_manifest.json len release !TAG!.
)

:done
echo.
echo ========================================================
echo   HOAN TAT! File game: %EXPORT_NAME%
echo   Phat hanh game bang GitHub Release kem update_manifest.json va cac patch PCK.
echo   Nguoi choi chi can tai/chay file exe; khong can Git hay .git.
echo ========================================================
echo.
pause
exit /b 0
