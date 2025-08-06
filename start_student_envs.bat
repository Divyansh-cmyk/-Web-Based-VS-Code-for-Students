@echo off
REM File: start_student_envs.bat
setlocal EnableDelayedExpansion
set NUM_STUDENTS=%1
set BASE_PORT=8080
set BASE_DIR=E:\student_workspaces

for /L %%i in (1,1,%NUM_STUDENTS%) do (
    set /A PORT=%BASE_PORT% + %%i
    set WORKSPACE=%BASE_DIR%\student_%%i
    mkdir !WORKSPACE!
    echo Starting container for Student %%i on port !PORT!
    docker run -d --name code_server_%%i ^
      -p !PORT!:8080 ^
      -v "!WORKSPACE!:/home/coder/project" ^
      -e PASSWORD=student%%i_pass ^
      codercom/code-server:latest ^
      --auth password
    echo Student %%i: http://%COMPUTERNAME%:!PORT!
)
endlocal