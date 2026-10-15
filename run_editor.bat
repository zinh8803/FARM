@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "GODOT_EXE="

:: 1. Kiem tra thu muc hien tai hoac thu muc cha
for %%f in ("%~dp0godot*.exe" "%~dp0..\godot*.exe") do (
    if exist "%%~f" (
        set "GODOT_EXE=%%~f"
        goto :found_godot
    )
)

:: 2. Kiem tra Downloads cua User hien tai
if exist "%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" (
    set "GODOT_EXE=%USERPROFILE%\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe"
    goto :found_godot
)

:: 3. Quet tim trong Downloads
for /r "%USERPROFILE%\Downloads" %%f in (Godot*win64*.exe) do (
    if exist "%%~f" (
        set "GODOT_EXE=%%~f"
        goto :found_godot
    )
)

:: 4. Kiem tra PATH
where godot >nul 2>&1
if not errorlevel 1 (
    set "GODOT_EXE=godot"
    goto :found_godot
)

echo [CANH BAO] Khong tim thay Godot Engine tren may.
pause
exit /b 1

:found_godot
start "" "!GODOT_EXE!" -e --path "%~dp0"
