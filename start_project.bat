@echo off
title CVS Monitoring - ONCF

echo ==========================================
echo       CVS MONITORING - ONCF
echo ==========================================
echo.

set PROJECT=C:\Users\DELL\Desktop\CVS_Monitoring

echo [1/5] Demarrage du broker MQTT...
start "MQTT Broker" cmd /k "mosquitto -v"

timeout /t 2 /nobreak >nul

echo [2/5] Demarrage du MQTT Subscriber...
start "MQTT Subscriber" cmd /k "cd /d %PROJECT% && venv\Scripts\activate && python -m communication.mqtt_subscriber"

timeout /t 2 /nobreak >nul

echo [3/5] Demarrage du simulateur CVS...
start "CVS Simulator" cmd /k "cd /d %PROJECT% && venv\Scripts\activate &&  python -m simulator.main  "

timeout /t 2 /nobreak >nul

echo [4/5] Demarrage de FastAPI...
start "FastAPI" cmd /k "cd /d %PROJECT% && venv\Scripts\activate && uvicorn api.main:app --reload"

timeout /t 3 /nobreak >nul

echo [5/5] Demarrage du Dashboard React...
start "React Dashboard" cmd /k "cd /d %PROJECT%\frontend && npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo ==========================================
echo       PROJET CVS DEMARRE
echo ==========================================
echo.
echo Dashboard :
echo http://localhost:5173
echo.
echo API :
echo http://127.0.0.1:8000/docs
echo.
pause