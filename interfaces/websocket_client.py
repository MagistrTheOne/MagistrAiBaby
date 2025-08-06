import asyncio
import websockets
import json
from config.settings import WS_HOST, WS_PORT
from interfaces.text_interface import TextInterface

class WebSocketClient:
    def __init__(self):
        self.text_interface = TextInterface()
        self.uri = f"ws://{WS_HOST}:{WS_PORT}"
    
    async def connect(self):
        """Connect to WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"Connected to {self.uri}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    async def listen(self):
        """Listen for incoming messages"""
        try:
            while True:
                message = await self.websocket.recv()
                await self.handle_message(message)
        except websockets.ConnectionClosed:
            print("Connection closed")
        except Exception as e:
            print(f"Error: {e}")
    
    async def handle_message(self, message):
        """Handle incoming message"""
        try:
            data = json.loads(message)
            
            if 'type' not in data:
                return
            
            if data['type'] == 'message':
                response = await self.text_interface.process_message(data['content'])
                await self.send_response(response)
                
            elif data['type'] == 'feedback':
                if 'score' in data:
                    self.text_interface.provide_feedback(float(data['score']))
                    
            elif data['type'] == 'get_history':
                history = self.text_interface.get_conversation_history()
                await self.send_history(history)
        
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error handling message: {e}")
    
    async def send_response(self, response):
        """Send response back to server"""
        message = {
            'type': 'response',
            'content': response
        }
        await self.websocket.send(json.dumps(message))
    
    async def send_history(self, history):
        """Send conversation history"""
        message = {
            'type': 'history',
            'content': history
        }
        await self.websocket.send(json.dumps(message))
    
    async def run(self):
        """Run the WebSocket client"""
        while True:
            connected = await self.connect()
            if connected:
                await self.listen()
            
            # If connection fails, wait before retrying
            await asyncio.sleep(5)

if __name__ == "__main__":
    client = WebSocketClient()
    asyncio.run(client.run())
