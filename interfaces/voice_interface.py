import whisper
import pyttsx3
import torch
import asyncio
import tempfile
import os
from typing import Optional, Any, Dict, TYPE_CHECKING
from config import (
    WHISPER_MODEL,
    VOICE_ENABLED,
    DEFAULT_VOICE_LANG,
    VOICE_SPEED
)

# Handle gTTS functionality
GTTS_AVAILABLE = False

if TYPE_CHECKING:
    from gtts import gTTS
else:
    try:
        from gtts import gTTS
        GTTS_AVAILABLE = True
    except ImportError:
        class gTTS:  # type: ignore
            def __init__(self, text: str, lang: str): ...
            def save(self, file_path: str): ...

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

class VoiceInterface:
    def __init__(self):
        """Initialize voice interface with Whisper model"""
        self.model = whisper.load_model(WHISPER_MODEL)
        self.voice_engine: Optional[Any] = None
        if VOICE_ENABLED:
            self.init_voice_engine()
    
    def init_voice_engine(self):
        """Initialize text-to-speech engine"""
        try:
            self.voice_engine = pyttsx3.init()
            self.voice_engine.setProperty('rate', VOICE_SPEED)
            
            # Try to find a natural-sounding voice
            voices = self.voice_engine.getProperty('voices')
            for voice in voices:
                if DEFAULT_VOICE_LANG in voice.languages:
                    self.voice_engine.setProperty('voice', voice.id)
                    break
        except:
            print("Warning: pyttsx3 initialization failed, falling back to gTTS")
            self.voice_engine = None
    
    async def listen(self):
        """Record and transcribe speech"""
        # Note: This is a placeholder. In a real implementation,
        # you would need to handle actual audio recording.
        # For now, we'll simulate with a dummy audio file
        try:
            result = self.model.transcribe("temp_audio.wav")
            return result["text"]
        except:
            return None
    
    async def speak(self, text):
        """Convert text to speech"""
        if not VOICE_ENABLED:
            print(f"[Voice disabled] Would say: {text}")
            return
        
        if self.voice_engine:
            # Use pyttsx3 for faster, offline TTS
            self.voice_engine.say(text)
            self.voice_engine.runAndWait()
        else:
            # Fallback to gTTS if available
            if GTTS_AVAILABLE:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                        tts = gTTS(text=text, lang=DEFAULT_VOICE_LANG)
                        tts.save(fp.name)
                        # Here you would play the audio file
                        # For now, we'll just print
                        print(f"[Voice] {text}")
                    os.unlink(fp.name)
                except Exception as e:
                    print(f"TTS Error: {e}")
                    print(f"[Voice failed] {text}")
            else:
                print(f"[Voice] {text} (gTTS not available)")
    
    async def process_speech(self, audio_input):
        """Process speech input and return text"""
        # Convert audio to text
        text = await self.listen()
        if not text:
            return None
            
        return text
    
    def adjust_voice(self, speed=None, volume=None):
        """Adjust voice parameters"""
        if not self.voice_engine:
            return
            
        if speed:
            self.voice_engine.setProperty('rate', speed)
        if volume:
            self.voice_engine.setProperty('volume', volume)
