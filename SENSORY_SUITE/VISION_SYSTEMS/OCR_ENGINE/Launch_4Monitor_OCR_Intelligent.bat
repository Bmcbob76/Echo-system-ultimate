@echo off
title 4-Monitor OCR Intelligent System Launcher
cls

echo ================================================================
echo     🎯 FOUR MONITOR OCR INTELLIGENT SYSTEM LAUNCHER
echo ================================================================
echo     Features: 4-Monitor OCR + Dual AI + Voice + Memory
echo     Foundation: GS343 + Phoenix 24/7 Protection 
echo ================================================================

cd /d "E:\ECHO_X_V2.0\SENSORY_SUITE_ULTIMATE\VISION_SYSTEMS\OCR_ENGINE"

echo.
echo 🔧 Checking Python environment...
python --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo 🔍 Installing required packages...
pip install pytesseract easyocr pillow opencv-python pyautogui pyttsx3 speechrecognition sounddevice numpy openai aiohttp --break-system-packages

echo.
echo 🔥 Starting Phoenix 24/7 Service...
cd /d "E:\ECHO_X_V2.0\GS343_DIVINE_OVERSIGHT\HEALERS"
call Phoenix_Control.ps1 -Action start

cd /d "E:\ECHO_X_V2.0\SENSORY_SUITE_ULTIMATE\VISION_SYSTEMS\OCR_ENGINE"

echo.
echo 🚀 Launching 4-Monitor OCR Intelligent System...
echo     Voice Control: Say "trinity", "echo prime", "hey echo", "analyze this"
echo     Interactive: Use coordination shell commands
echo     Monitoring: 4 monitors with dual AI analysis
echo.

REM Start the coordination system
python ocr_intelligence_coordinator.py

echo.
echo ✅ 4-Monitor OCR Intelligent System stopped
pause
