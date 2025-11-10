"""
🎤 ECHO VOICE SYSTEM
Wake word: "ECHO"
Personality: Confident, loyal, protective partner
"""
import asyncio
import logging
from pathlib import Path
from typing import Optional
import speech_recognition as sr
from AGENT_PERSONALITIES.echo_prime_personality import EchoPrimePersonality
from AGENT_PERSONALITIES.voice_cache_system import VoiceCacheSystem

class EchoVoiceSystem:
    """ECHO voice control system"""
    
    def __init__(self):
        self.wake_word = "ECHO"
        self.listening = False
        self.personality = EchoPrimePersonality()
        self.voice_cache = VoiceCacheSystem()
        self.recognizer = sr.Recognizer()
        self.logger = logging.getLogger(__name__)
        
    async def start_listening(self):
        """Start listening for wake word"""
        self.listening = True
        self.logger.info(f"🎤 Listening for wake word: {self.wake_word}")
        
        while self.listening:
            try:
                with sr.Microphone() as source:
                    self.logger.info("🎧 Listening...")
                    audio = self.recognizer.listen(source, timeout=5)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    self.logger.info(f"📢 Heard: {text}")
                    
                    # Check for wake word
                    if self.wake_word.lower() in text.lower():
                        await self._handle_command(text)
                        
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                self.logger.error(f"❌ Voice error: {e}")
                await asyncio.sleep(1)
                
    async def _handle_command(self, text: str):
        """Handle voice command"""
        self.logger.info(f"🎤 Processing command: {text}")
        
        # Generate response with personality
        response = await self.personality.generate_response(text)
        
        # Speak response
        await self.speak(response)
        
    async def speak(self, text: str):
        """Speak response using ECHO voice"""
        self.logger.info(f"🔊 Speaking: {text}")
        
        try:
            # Use voice cache system
            audio_path = await self.voice_cache.get_or_generate(
                text=text,
                personality="echo_prime"
            )
            
            # Play audio (implement based on your TTS system)
            self.logger.info(f"🔊 Playing: {audio_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Speech error: {e}")
    
    def stop_listening(self):
        """Stop listening"""
        self.listening = False
        self.logger.info("🎤 Stopped listening")

# Voice command patterns
COMMAND_PATTERNS = {
    'code': ['code', 'program', 'script', 'build', 'write'],
    'money': ['money', 'trade', 'profit', 'revenue', 'arbitrage'],
    'protect': ['protect', 'defend', 'secure', 'threat', 'attack'],
    'harvest': ['harvest', 'research', 'learn', 'study', 'knowledge'],
    'status': ['status', 'report', 'health', 'systems']
}
