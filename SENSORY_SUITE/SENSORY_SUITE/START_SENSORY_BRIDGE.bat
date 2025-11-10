@echo off
title SENSORY SUITE - AUTO LAUNCHER
color 0A

echo ============================================
echo    SENSORY SUITE INTEGRATION
echo    Authority Level 11.0 - Commander Mode
echo ============================================
echo.

echo [STEP 1/3] Activating Sensory Bridge API...
echo Starting: http://localhost:8343
echo.
start "Sensory Bridge API" H:\Tools\python.exe "P:\ECHO_PRIME\SENSORY_SUITE\sensory_bridge_api.py"

timeout /t 3 /nobreak >nul

echo [STEP 2/3] Verifying connection...
curl -s http://localhost:8343/health
echo.

echo [STEP 3/3] Ready for GUI integration!
echo.
echo ============================================
echo AVAILABLE SENSORS:
echo   [VOICE]    - ElevenLabs V3 + IndexTTS
echo   [VISION]   - Webcam + Face Detection
echo   [HEARING]  - Microphone + Audio Analysis
echo   [OCR]      - Multi-Monitor Screen Reading
echo   [CPU]      - Direct Hardware Control
echo   [INTERNET] - Network Access
echo ============================================
echo.
echo API Endpoints:
echo   - http://localhost:8343/health
echo   - http://localhost:8343/sensors/status
echo   - http://localhost:8343/sensors/toggle
echo   - http://localhost:8343/voice/speak
echo   - http://localhost:8343/vision/capture
echo   - http://localhost:8343/ocr/scan
echo.
echo Press any key to stop Sensory Bridge...
pause >nul

taskkill /F /FI "WINDOWTITLE eq Sensory Bridge API*"
echo.
echo Sensory Bridge stopped.
pause