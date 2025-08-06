import asyncio
import websockets
import json
from typing import Set, Dict, Any
from config import (
    WS_HOST,
    WS_PORT,
    VOICE_ENABLED,
    DEFAULT_VOICE_LANG
)
from interfaces.text_interface import TextInterface
from interfaces.voice_interface import VoiceInterface

class BabyBrainServer:
    def __init__(self):
        self.text_interface = TextInterface()
        self.voice_interface = VoiceInterface()
        self.clients = set()
    
    async def register(self, websocket):
        """Register a new client"""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        finally:
            self.clients.remove(websocket)
    
    async def handle_message(self, websocket, message):
        """Handle incoming message"""
        try:
            data = json.loads(message)
            
            if 'type' not in data:
                return
            
            response = None
            
            if data['type'] == 'text':
                response = await self.text_interface.process_message(data['content'])
                
            elif data['type'] == 'voice':
                # Process voice input
                text = await self.voice_interface.process_speech(data['content'])
                if text:
                    response = await self.text_interface.process_message(text)
                    # Convert response to speech
                    await self.voice_interface.speak(response)
                
            elif data['type'] == 'feedback':
                if 'score' in data:
                    self.text_interface.provide_feedback(float(data['score']))
                    response = "Feedback received"
            
            if response:
                await self.send_response(websocket, response)
        
        except json.JSONDecodeError:
            await self.send_error(websocket, "Invalid JSON format")
        except Exception as e:
            await self.send_error(websocket, str(e))
    
    async def send_response(self, websocket, response):
        """Send response to client"""
        message = {
            'type': 'response',
            'content': response
        }
        await websocket.send(json.dumps(message))
    
    async def send_error(self, websocket, error):
        """Send error message to client"""
        message = {
            'type': 'error',
            'content': error
        }
        await websocket.send(json.dumps(message))
    
    async def start(self):
        """Start the WebSocket server"""
        async with websockets.serve(self.register, WS_HOST, WS_PORT):
            print(f"Server running on ws://{WS_HOST}:{WS_PORT}")
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    server = BabyBrainServer()
    asyncio.run(server.start())
