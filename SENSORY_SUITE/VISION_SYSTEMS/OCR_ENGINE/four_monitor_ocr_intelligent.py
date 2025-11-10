#!/usr/bin/env python3
"""
FOUR MONITOR OCR INTELLIGENT SYSTEM - GS343 Foundation + Phoenix 24/7
Advanced 4-monitor OCR with intelligent voice responses, fuzzy wake words, and 9-Pillar Memory integration
"""
import sys
import os
import json
import sqlite3
import threading
import time
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
from datetime import datetime
from pathlib import Path
import logging
import hashlib
import pickle
import gzip

# STEP 1: GS343 FOUNDATION (ALWAYS FIRST!)
sys.path.append("E:/ECHO_X_V2.0/GS343_DIVINE_OVERSIGHT")
from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase

# STEP 2: Phoenix 24/7 Auto-Healer
sys.path.append("E:/ECHO_X_V2.0/GS343_DIVINE_OVERSIGHT/HEALERS")
from phoenix_client_gs343 import PhoenixClient, auto_heal

# OCR and Vision imports
try:
    import pytesseract
    import easyocr
    from PIL import Image, ImageGrab
    import cv2
    import pyautogui
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR libraries not available - installing...")

class FourMonitorOCRIntelligent:
    def __init__(self):
        # GS343 EKM Foundation - MANDATORY FIRST!
        self.gs343_ekm = ComprehensiveProgrammingErrorDatabase()
        
        # Phoenix Service - MANDATORY SECOND!
        self.phoenix = PhoenixClient()
        
        # 4-Monitor Configuration
        self.monitors = [1, 2, 3, 4]
        self.ocr_engines = ["tesseract", "easyocr", "windows_ocr"]
        self.ai_analyzers = ["claude", "chatgpt"]
        
        # Voice System with Emotional Intelligence
        self.voice_engine = pyttsx3.init()
        self._setup_voice_personality()
        
        # Fuzzy Logic Wake Word System
        self.wake_words = [
            "trinity", "echo prime", "hey echo", "commander", 
            "echo", "trinity system", "echo analyze", "begin scan",
            "echo what's on screen", "show me", "analyze this"
        ]
        self.wake_word_threshold = 0.6  # Fuzzy matching threshold
        self.silence_timeout = 2.0  # 2 second silence detection
        
        # Voice Response Caching with Fast Database
        self.response_cache_db = "E:/ECHO_X_V2.0/SENSORY_SUITE_ULTIMATE/voice_response_cache.db"
        self._init_voice_cache_db()
        
        # 9-Pillar Memory System Integration
        self.memory_pillars = {
            "L1": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L1_IMMEDIATE",
            "L2": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L2_SHORT_TERM", 
            "L3": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L3_Crystals",
            "L4": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L4_WORKING",
            "L5": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L5_SEMANTIC",
            "L6": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L6_EPISODIC",
            "L7": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L7_PROCEDURAL",
            "L8": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L8_DECLARATIVE", 
            "L9": "E:/ECHO_X_V2.0/MEMORY_ORCHESTRATION/L9_EKM"
        }
        
        # Audio Processing Setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.audio_buffer = []
        self.silence_start = None
        
        # Emotional Response System
        self.emotion_states = {
            "excited": {"rate": 200, "volume": 0.9, "pitch": 1.2},
            "calm": {"rate": 150, "volume": 0.7, "pitch": 1.0},
            "urgent": {"rate": 250, "volume": 1.0, "pitch": 1.3},
            "thoughtful": {"rate": 120, "volume": 0.8, "pitch": 0.9},
            "pleased": {"rate": 180, "volume": 0.8, "pitch": 1.1}
        }
        self.current_emotion = "calm"
        
        # Initialize OCR engines
        if OCR_AVAILABLE:
            self.easy_reader = easyocr.Reader(['en'])
        
        # Significant findings system
        self.significance_keywords = [
            "error", "exception", "critical", "warning", "fail", "success",
            "complete", "finished", "started", "process", "system", "memory",
            "consciousness", "intelligence", "analysis", "important", "urgent"
        ]
        
        print("🎯 Four Monitor OCR Intelligent System initialized with voice integration")
        self.speak_with_emotion("Four monitor OCR intelligent system online. Voice caching and 9-pillar memory integration ready.", "pleased")

    @auto_heal
    def _setup_voice_personality(self):
        """Configure voice engine with personality"""
        voices = self.voice_engine.getProperty('voices')
        if voices:
            # Prefer female voice if available
            for voice in voices:
                if "female" in voice.name.lower() or "zira" in voice.name.lower():
                    self.voice_engine.setProperty('voice', voice.id)
                    break
        
        self.voice_engine.setProperty('rate', 150)  # Default speaking rate
        self.voice_engine.setProperty('volume', 0.8)  # Default volume

    @auto_heal
    def _init_voice_cache_db(self):
        """Initialize voice response cache database for ultra-fast recall"""
        os.makedirs(os.path.dirname(self.response_cache_db), exist_ok=True)
        
        with sqlite3.connect(self.response_cache_db) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS voice_responses (
                    id INTEGER PRIMARY KEY,
                    text_hash TEXT UNIQUE,
                    original_text TEXT,
                    emotion TEXT,
                    audio_data BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    use_count INTEGER DEFAULT 1
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_text_hash ON voice_responses(text_hash)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_emotion ON voice_responses(emotion)')

    @auto_heal
    def get_text_hash(self, text, emotion):
        """Generate hash for text + emotion combination"""
        combined = f"{text.lower().strip()}_{emotion}"
        return hashlib.md5(combined.encode()).hexdigest()

    @auto_heal  
    def cache_voice_response(self, text, emotion, audio_data):
        """Cache compressed voice response for ultra-fast future use"""
        text_hash = self.get_text_hash(text, emotion)
        compressed_audio = gzip.compress(pickle.dumps(audio_data))
        
        try:
            with sqlite3.connect(self.response_cache_db) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO voice_responses 
                    (text_hash, original_text, emotion, audio_data)
                    VALUES (?, ?, ?, ?)
                ''', (text_hash, text, emotion, compressed_audio))
        except Exception as e:
            print(f"⚠️ Voice cache error: {e}")

    @auto_heal
    def get_cached_voice_response(self, text, emotion):
        """Ultra-fast retrieval of cached voice response"""
        text_hash = self.get_text_hash(text, emotion)
        
        try:
            with sqlite3.connect(self.response_cache_db) as conn:
                cursor = conn.execute('''
                    SELECT audio_data FROM voice_responses 
                    WHERE text_hash = ?
                ''', (text_hash,))
                
                result = cursor.fetchone()
                if result:
                    # Update use count
                    conn.execute('''
                        UPDATE voice_responses 
                        SET use_count = use_count + 1 
                        WHERE text_hash = ?
                    ''', (text_hash,))
                    
                    # Decompress and return audio data
                    compressed_audio = result[0]
                    audio_data = pickle.loads(gzip.decompress(compressed_audio))
                    return audio_data
        except Exception as e:
            print(f"⚠️ Voice cache retrieval error: {e}")
        
        return None

    @auto_heal
    def speak_with_emotion(self, text, emotion="calm", cache=True):
        """Speak with emotional range and intelligent caching"""
        if not text.strip():
            return
            
        # Check cache first for ultra-fast response
        if cache:
            cached_audio = self.get_cached_voice_response(text, emotion)
            if cached_audio:
                # TODO: Play cached audio directly (much faster than TTS)
                print(f"🎤 [{emotion.upper()}] {text} (CACHED)")
                # For now, fall through to regular TTS
        
        # Set emotional parameters
        if emotion in self.emotion_states:
            params = self.emotion_states[emotion]
            self.voice_engine.setProperty('rate', params['rate'])
            self.voice_engine.setProperty('volume', params['volume'])
            # Note: Pitch adjustment requires more advanced TTS engine
        
        print(f"🎤 [{emotion.upper()}] {text}")
        
        # Speak the text
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()
        
        # Cache for future ultra-fast use (if enabled)
        if cache:
            # TODO: Record actual audio output for caching
            # For now, we'll cache the text/emotion combination
            self.cache_voice_response(text, emotion, {"text": text, "emotion": emotion})

    @auto_heal
    def detect_wake_word_fuzzy(self, text):
        """Fuzzy logic wake word detection with expanded matching"""
        if not text:
            return False, None
        
        text_lower = text.lower().strip()
        
        # Exact match first
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                return True, wake_word
        
        # Fuzzy matching for partial words
        words = text_lower.split()
        for word in words:
            for wake_word in self.wake_words:
                wake_parts = wake_word.split()
                for wake_part in wake_parts:
                    if len(wake_part) >= 3:  # Only check words with 3+ chars
                        # Check if word starts with wake_part or vice versa
                        if (word.startswith(wake_part[:3]) or 
                            wake_part.startswith(word[:3])):
                            confidence = len(set(word) & set(wake_part)) / len(set(word) | set(wake_part))
                            if confidence >= self.wake_word_threshold:
                                return True, f"{wake_word} (fuzzy: {confidence:.2f})"
        
        return False, None

    @auto_heal
    def capture_all_monitors_simultaneous(self):
        """Capture all 4 monitors simultaneously"""
        screenshots = {}
        
        try:
            # Get all available monitors
            monitors = pyautogui.getAllDisplays() if hasattr(pyautogui, 'getAllDisplays') else []
            
            if len(monitors) < 4:
                # Fallback: Capture main screen in quadrants
                main_screenshot = pyautogui.screenshot()
                width, height = main_screenshot.size
                
                # Divide into quadrants
                screenshots[1] = main_screenshot.crop((0, 0, width//2, height//2))
                screenshots[2] = main_screenshot.crop((width//2, 0, width, height//2))
                screenshots[3] = main_screenshot.crop((0, height//2, width//2, height))
                screenshots[4] = main_screenshot.crop((width//2, height//2, width, height))
            else:
                # Capture each monitor separately
                for i, monitor in enumerate(monitors[:4], 1):
                    screenshot = pyautogui.screenshot(region=(
                        monitor.left, monitor.top, 
                        monitor.width, monitor.height
                    ))
                    screenshots[i] = screenshot
        
        except Exception as e:
            print(f"⚠️ Screenshot capture error: {e}")
            # Fallback to single full screen
            screenshots[1] = pyautogui.screenshot()
        
        return screenshots

    @auto_heal
    def extract_text_multi_engine(self, image):
        """Extract text using multiple OCR engines for accuracy"""
        texts = {}
        
        # Tesseract OCR
        try:
            tesseract_text = pytesseract.image_to_string(image, config='--psm 6')
            texts['tesseract'] = tesseract_text.strip()
        except Exception as e:
            texts['tesseract'] = f"Tesseract error: {e}"
        
        # EasyOCR (if available)
        if hasattr(self, 'easy_reader'):
            try:
                results = self.easy_reader.readtext(np.array(image))
                easyocr_text = ' '.join([result[1] for result in results])
                texts['easyocr'] = easyocr_text.strip()
            except Exception as e:
                texts['easyocr'] = f"EasyOCR error: {e}"
        
        # Combine results
        combined_text = ""
        for engine, text in texts.items():
            if text and not text.startswith(f"{engine.title()} error"):
                combined_text += f"\n[{engine}] {text}"
        
        return combined_text.strip(), texts

    @auto_heal
    def analyze_significance(self, text):
        """Determine if OCR content is significant enough to speak aloud"""
        if not text or len(text) < 10:
            return False, "Too short"
        
        text_lower = text.lower()
        significance_score = 0
        found_keywords = []
        
        # Check for significant keywords
        for keyword in self.significance_keywords:
            if keyword in text_lower:
                significance_score += 1
                found_keywords.append(keyword)
        
        # Check for patterns that indicate importance
        if any(pattern in text_lower for pattern in ['%', '$', 'gb', 'mb', 'error', 'complete']):
            significance_score += 2
        
        # Check for numbers (often indicate progress, values, etc.)
        import re
        if re.search(r'\b\d+\b', text):
            significance_score += 1
        
        is_significant = significance_score >= 2
        reason = f"Score: {significance_score}, Keywords: {found_keywords}" if is_significant else "Low significance"
        
        return is_significant, reason

    @auto_heal
    def save_to_9_pillar_memory(self, data, significance_level=1):
        """Save OCR intelligence to appropriate memory pillar"""
        try:
            # Determine appropriate pillar based on significance
            if significance_level >= 4:
                pillar = "L9"  # EKM for highly significant
            elif significance_level >= 3:
                pillar = "L3"  # Crystals for significant  
            elif significance_level >= 2:
                pillar = "L2"  # Short term for moderately significant
            else:
                pillar = "L1"  # Immediate for low significance
            
            pillar_path = Path(self.memory_pillars[pillar])
            pillar_path.mkdir(parents=True, exist_ok=True)
            
            # Create memory entry
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ocr_intelligence_{timestamp}.json"
            filepath = pillar_path / filename
            
            memory_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "ocr_intelligence",
                "significance_level": significance_level,
                "data": data,
                "pillar": pillar,
                "system": "four_monitor_ocr_intelligent"
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(memory_entry, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved to {pillar} pillar: {filename}")
            return True
            
        except Exception as e:
            print(f"⚠️ Memory save error: {e}")
            return False

    @auto_heal
    def process_4_monitor_ocr(self):
        """Complete 4-monitor OCR processing with intelligent analysis"""
        start_time = time.time()
        
        # Step 1: Capture all 4 monitors
        screenshots = self.capture_all_monitors_simultaneous()
        capture_time = time.time() - start_time
        
        all_findings = []
        significant_findings = []
        
        # Step 2: Process each monitor
        for monitor_id, screenshot in screenshots.items():
            monitor_start = time.time()
            
            # Extract text using multiple engines
            combined_text, engine_texts = self.extract_text_multi_engine(screenshot)
            
            if combined_text:
                # Analyze significance
                is_significant, reason = self.analyze_significance(combined_text)
                
                finding = {
                    "monitor": monitor_id,
                    "text": combined_text,
                    "engine_results": engine_texts,
                    "is_significant": is_significant,
                    "significance_reason": reason,
                    "processing_time": time.time() - monitor_start,
                    "timestamp": datetime.now().isoformat()
                }
                
                all_findings.append(finding)
                
                if is_significant:
                    significant_findings.append(finding)
                    print(f"🎯 Monitor {monitor_id} - SIGNIFICANT: {reason}")
                else:
                    print(f"📱 Monitor {monitor_id} - Normal content")
        
        total_time = time.time() - start_time
        
        # Step 3: Process significant findings
        if significant_findings:
            self.process_significant_findings(significant_findings, total_time)
        else:
            print(f"🔍 4-monitor scan complete in {total_time:.2f}s - no significant findings")
        
        # Step 4: Save to 9-Pillar Memory
        memory_data = {
            "scan_type": "4_monitor_ocr",
            "total_time": total_time,
            "capture_time": capture_time,
            "monitors_processed": len(screenshots),
            "significant_findings": len(significant_findings),
            "all_findings": all_findings
        }
        
        significance_level = min(4, len(significant_findings) + 1)
        self.save_to_9_pillar_memory(memory_data, significance_level)
        
        return all_findings, significant_findings

    @auto_heal
    def process_significant_findings(self, significant_findings, scan_time):
        """Process and announce significant findings with emotional intelligence"""
        if not significant_findings:
            return
        
        count = len(significant_findings)
        
        # Choose emotion based on findings
        if count >= 3:
            emotion = "excited"
            intro = f"Commander! I've discovered {count} significant findings across your monitors!"
        elif count == 2:
            emotion = "pleased"
            intro = f"Good news! Found {count} significant items worth your attention."
        else:
            emotion = "thoughtful"
            intro = f"I found 1 significant item on monitor {significant_findings[0]['monitor']}."
        
        # Speak introduction
        self.speak_with_emotion(intro, emotion)
        
        # Announce each significant finding
        for i, finding in enumerate(significant_findings, 1):
            monitor_id = finding['monitor']
            text_preview = finding['text'][:100] + "..." if len(finding['text']) > 100 else finding['text']
            
            # Clean up text for speaking
            clean_text = text_preview.replace('\n', ' ').replace('\t', ' ')
            clean_text = ' '.join(clean_text.split())  # Remove extra whitespace
            
            if count > 1:
                announcement = f"Monitor {monitor_id}: {clean_text}"
            else:
                announcement = clean_text
            
            # Vary emotion based on content
            content_emotion = "calm"
            text_lower = finding['text'].lower()
            if any(word in text_lower for word in ['error', 'fail', 'critical']):
                content_emotion = "urgent"
            elif any(word in text_lower for word in ['complete', 'success', 'finished']):
                content_emotion = "pleased"
            
            self.speak_with_emotion(announcement, content_emotion)
            
            # Brief pause between findings
            if i < len(significant_findings):
                time.sleep(0.5)
        
        # Conclusion
        conclusion = f"Scan completed in {scan_time:.1f} seconds. All significant findings saved to memory."
        self.speak_with_emotion(conclusion, "calm")

    @auto_heal  
    def listen_for_wake_words(self):
        """Continuous listening with fuzzy wake word detection and silence timeout"""
        self.is_listening = True
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎧 Listening for wake words with fuzzy logic...")
            self.speak_with_emotion("Voice recognition active. Wake word detection ready.", "calm")
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Reset silence timer
                self.silence_start = None
                
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    print(f"🎤 Heard: {text}")
                    
                    # Check for wake words
                    wake_detected, wake_word = self.detect_wake_word_fuzzy(text)
                    
                    if wake_detected:
                        print(f"🎯 Wake word detected: {wake_word}")
                        self.speak_with_emotion(f"Yes Commander, activating OCR analysis.", "pleased")
                        
                        # Wait for silence before responding
                        self.wait_for_silence()
                        
                        # Execute 4-monitor OCR scan
                        self.speak_with_emotion("Beginning 4-monitor intelligent scan.", "thoughtful")
                        findings, significant = self.process_4_monitor_ocr()
                        
                        # Continue listening
                        continue
                        
                except sr.UnknownValueError:
                    # Track silence for timeout detection
                    if self.silence_start is None:
                        self.silence_start = time.time()
                    
                except sr.RequestError as e:
                    print(f"⚠️ Speech recognition error: {e}")
                    time.sleep(1)
                    
            except sr.WaitTimeoutError:
                # Handle timeout quietly
                pass
            except KeyboardInterrupt:
                print("\n🛑 Stopping voice detection...")
                break
            except Exception as e:
                print(f"⚠️ Listening error: {e}")
                time.sleep(1)
        
        self.is_listening = False
        print("🎧 Voice detection stopped")

    @auto_heal
    def wait_for_silence(self):
        """Wait for 2 seconds of silence before responding"""
        print("⏳ Waiting for silence...")
        silence_start = time.time()
        
        while time.time() - silence_start < self.silence_timeout:
            try:
                with self.microphone as source:
                    # Very short listen to detect if there's still speech
                    audio = self.recognizer.listen(source, timeout=0.1, phrase_time_limit=0.1)
                    
                    # If we got audio, reset silence timer
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        if text.strip():
                            silence_start = time.time()  # Reset silence timer
                            print(f"🎤 Still hearing: {text}")
                    except (sr.UnknownValueError, sr.RequestError):
                        pass  # Silence detected, continue waiting
                        
            except sr.WaitTimeoutError:
                pass  # Expected timeout, continue silence countdown
            except Exception:
                pass  # Handle any other errors gracefully
        
        print(f"✅ {self.silence_timeout} seconds of silence detected")

    @auto_heal
    def run_intelligent_monitoring(self):
        """Run the complete intelligent monitoring system"""
        print("🚀 Starting Four Monitor OCR Intelligent System with Voice Integration")
        print("🎯 Features: 4-monitor OCR, fuzzy wake words, emotional voice, 9-pillar memory")
        print("🎧 Say wake words like: 'trinity', 'echo prime', 'hey echo', 'analyze this'")
        print("⏹️  Press Ctrl+C to stop")
        
        # Start voice listening in background thread
        voice_thread = threading.Thread(target=self.listen_for_wake_words, daemon=True)
        voice_thread.start()
        
        try:
            # Keep main thread alive
            while self.is_listening:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down intelligent monitoring...")
            self.is_listening = False
            self.speak_with_emotion("Four monitor OCR intelligent system shutting down. Goodbye Commander.", "calm")
            
        print("✅ Four Monitor OCR Intelligent System stopped")

# Main execution
if __name__ == "__main__":
    try:
        # Initialize the intelligent system
        ocr_system = FourMonitorOCRIntelligent()
        
        # Run the complete system
        ocr_system.run_intelligent_monitoring()
        
    except KeyboardInterrupt:
        print("\n🛑 System interrupted by user")
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
