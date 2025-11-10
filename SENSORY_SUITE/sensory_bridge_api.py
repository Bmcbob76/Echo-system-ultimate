#!/usr/bin/env python3
"""
🎯 SENSORY SUITE AUTO-LAUNCHER
Integrates P:\ECHO_PRIME\SENSORY_SUITE with Master GUI
Authority Level 11.0
"""
import sys
import os
import asyncio
import json
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading

# Add paths
sys.path.append("P:/ECHO_PRIME/SENSORY_SUITE/SENSORY_SYSTEMS")
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343")

# Import sensory system
from ultra_sensory_system import UltraSensorySystem

# Import GS343 Foundation
from gs343_foundation import GS343Foundation

class SensoryBridge:
    """Bridge between Sensory Suite and Master GUI"""
    
    def __init__(self):
        """Initialize Sensory Bridge"""
        self.app = Flask(__name__)
        CORS(self.app)
        
        # GS343 Foundation
        self.gs343 = GS343Foundation()
        
        # Initialize sensory system
        print("🎯 Initializing Sensory Suite...")
        self.sensory = UltraSensorySystem()
        
        # Sensor states
        self.sensors = {
            "voice": False,
            "vision": False,
            "hearing": False,
            "ocr": False,
            "cpu": True,
            "internet": True
        }
        
        # Setup routes
        self._setup_routes()
        
        print("✅ Sensory Bridge initialized")
        print("🌐 API available at: http://localhost:8343")
    
    def _setup_routes(self):
        """Setup Flask API routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint"""
            return jsonify({
                "status": "online",
                "service": "Sensory Bridge",
                "port": 8343,
                "sensors": self.sensors
            })
        
        @self.app.route('/sensors/status', methods=['GET'])
        def sensor_status():
            """Get all sensor statuses"""
            return jsonify({
                "voice": {
                    "enabled": self.sensors["voice"],
                    "models": ["indextts", "elevenlabs_v3"],
                    "status": "ready"
                },
                "vision": {
                    "enabled": self.sensors["vision"],
                    "cameras": ["primary_webcam"],
                    "resolution": [1920, 1080],
                    "status": "ready"
                },
                "hearing": {
                    "enabled": self.sensors["hearing"],
                    "microphones": ["default"],
                    "status": "ready"
                },
                "ocr": {
                    "enabled": self.sensors["ocr"],
                    "engines": ["tesseract", "paddleocr"],
                    "monitors": 3,
                    "status": "ready"
                },
                "cpu_control": {
                    "enabled": self.sensors["cpu"],
                    "status": "ready"
                },
                "internet": {
                    "enabled": self.sensors["internet"],
                    "status": "connected"
                }
            })
        
        @self.app.route('/sensors/toggle', methods=['POST'])
        def toggle_sensor():
            """Toggle sensor on/off"""
            data = request.json
            sensor = data.get('sensor')
            enabled = data.get('enabled')
            
            if sensor not in self.sensors:
                return jsonify({"error": "Invalid sensor"}), 400
            
            # Update sensor state
            self.sensors[sensor] = enabled
            
            # Activate/deactivate sensor in sensory system
            if sensor == "voice":
                self.sensory.voice_enabled = enabled
            elif sensor == "vision":
                self.sensory.vision_enabled = enabled
            elif sensor == "hearing":
                self.sensory.hearing_enabled = enabled
            
            return jsonify({
                "sensor": sensor,
                "enabled": enabled,
                "message": f"Sensor {sensor} {'enabled' if enabled else 'disabled'}"
            })
        
        @self.app.route('/voice/speak', methods=['POST'])
        def speak():
            """Speak text using voice system"""
            data = request.json
            text = data.get('text')
            voice = data.get('voice', 'echo')
            
            # Use sensory system to speak
            # This will use IndexTTS or ElevenLabs V3
            result = self.sensory.speak(text, voice)
            
            return jsonify({
                "text": text,
                "voice": voice,
                "status": "speaking"
            })
        
        @self.app.route('/vision/capture', methods=['GET'])
        def capture():
            """Capture image from webcam"""
            if not self.sensors["vision"]:
                return jsonify({"error": "Vision not enabled"}), 400
            
            # Capture from sensory system
            image_data = self.sensory.capture_image()
            
            return jsonify({
                "status": "captured",
                "resolution": [1920, 1080],
                "timestamp": str(asyncio.get_event_loop().time())
            })
        
        @self.app.route('/ocr/scan', methods=['GET'])
        def ocr_scan():
            """Scan screen with OCR"""
            if not self.sensors["ocr"]:
                return jsonify({"error": "OCR not enabled"}), 400
            
            # Scan all monitors
            monitor = request.args.get('monitor', 'all')
            
            # Use sensory system OCR
            text = self.sensory.ocr_scan(monitor)
            
            return jsonify({
                "monitor": monitor,
                "text": text,
                "timestamp": str(asyncio.get_event_loop().time())
            })
    
    def run(self):
        """Run the Flask server"""
        print("🚀 Starting Sensory Bridge Server...")
        print("🌐 Listening on: http://localhost:8343")
        print("📡 GUI can now control all sensors")
        self.app.run(host='0.0.0.0', port=8343, debug=False)

if __name__ == "__main__":
    print("=" * 60)
    print("🎖️ SENSORY SUITE BRIDGE - AUTHORITY LEVEL 11.0")
    print("=" * 60)
    print()
    
    # Initialize and run
    bridge = SensoryBridge()
    bridge.run()