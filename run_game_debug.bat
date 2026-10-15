@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================================
echo   KHOI DONG GAME NONG TRAI (CHE DO DEBUG CONSOLE)
echo ========================================================

set "GODOT_CONSOLE="

:: 1. Kiem tra Godot trong thu muc project hoac thu muc cha
for %%f in ("%~dp0godot*console*.exe" "%~dp0..\godot*console*.exe") do (
    if exist "%%~f" (
        set "GODOT_CONSOLE=%%~f"
        goto :found_godot
    )
)

:: 2. Kiem tra Downloads cua User hien tai
if exist "%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe" (
    set "GODOT_CONSOLE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe"
    goto :found_godot
)

:: 3. Quet tim trong Downloads
for /r "%USERPROFILE%\Downloads" %%f in (*console*.exe) do (
    if exist "%%~f" (
        set "GODOT_CONSOLE=%%~f"
        goto :found_godot
    )
)

:: 4. Kiem tra PATH
where godot >nul 2>&1
if not errorlevel 1 (
    set "GODOT_CONSOLE=godot"
    goto :found_godot
)

echo [CANH BAO] Khong tim thay Godot Console tren may.
pause
exit /b 1

:found_godot
echo Chay debug voi: "!GODOT_CONSOLE!"
"!GODOT_CONSOLE!" --path "%~dp0" --verbose
pause
