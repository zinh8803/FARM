@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================================
echo        KHOI DONG GAME NONG TRAI VIET (GODOT 4)
echo ========================================================
echo Dang khoi chay game...

set "GODOT_EXE="

:: 1. Kiem tra Godot trong thu muc project hoac thu muc cha
for %%f in ("%~dp0godot*.exe" "%~dp0..\godot*.exe") do (
    if exist "%%~f" (
        set "GODOT_EXE=%%~f"
        goto :found_godot
    )
)

:: 2. Kiem tra Godot trong thu muc Downloads cua User hien tai (%USERPROFILE%\Downloads)
if exist "%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" (
    set "GODOT_EXE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe"
    goto :found_godot
)
if exist "%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe" (
    set "GODOT_EXE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe"
    goto :found_godot
)

:: 3. Quet tim bat ky file Godot*win64.exe nao trong Downloads
for /r "%USERPROFILE%\Downloads" %%f in (Godot*win64*.exe) do (
    if exist "%%~f" (
        set "GODOT_EXE=%%~f"
        goto :found_godot
    )
)

:: 4. Kiem tra lenh godot trong PATH
where godot >nul 2>&1
if not errorlevel 1 (
    set "GODOT_EXE=godot"
    goto :found_godot
)

echo [CANH BAO] Khong tim thay file thuc thi Godot tren may.
echo Vui long dat file godot.exe vao thu muc game hoac thu muc Downloads cua ban.
pause
exit /b 1

:found_godot
echo Khoi dong game truc tiep voi: "!GODOT_EXE!"
start "" "!GODOT_EXE!" --path "%~dp0"
exit /b 0
