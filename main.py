import asyncio
import argparse
import logging
from typing import Optional, Union, NoReturn
from pathlib import Path
from interfaces.text_interface import TextInterface
from interfaces.voice_interface import VoiceInterface
from baby_brain_server import BabyBrainServer
from core.agent_state import AgentState
from agents.cognitive_agent import CognitiveAgent
from config.settings import BRAIN_STATE_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BabyTrainer:
    def __init__(self, save_dir: Union[str, Path]):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.save_dir / "baby_state.pkl"
        self.agent = CognitiveAgent(state_path=self.state_path)
        self.state = AgentState()
    
    async def start_training(self, mode: str) -> None:
        """Start training the baby in specified mode"""
        if mode == 'text':
            interface = TextInterface()
            await interface.interactive_session()
        
        elif mode == 'voice':
            interface = VoiceInterface()
            print("Voice interface started. Speak to interact.")
            while True:
                text = await interface.listen()
                if text:
                    print(f"You said: {text}")
                    response = self.agent.process_input(text)
                    await interface.speak(response)
        
        elif mode == 'server':
            server = BabyBrainServer()
            await server.start()
    
    def save_state(self) -> None:
        """Save current baby state"""
        self.agent.save_state(self.state_path)
    
    def load_state(self) -> bool:
        """Load previous baby state if exists"""
        if self.state_path.exists():
            return self.agent.load_state(self.state_path)
        return False

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        "data",
        "data/brain_state",
        "data/memories",
        "data/iterations"
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

async def main() -> None:
    parser = argparse.ArgumentParser(description='AI Baby Brain Training System')
    parser.add_argument(
        '--mode', 
        choices=['text', 'voice', 'server'], 
        default='text', 
        help='Training interface mode'
    )
    parser.add_argument(
        '--load', 
        action='store_true',
        help='Load previous baby state'
    )
    args = parser.parse_args()
    
    # Ensure all required directories exist
    ensure_directories()
    
    trainer = None
    try:
        logging.info("Initializing AI Baby Brain Training System...")
        trainer = BabyTrainer(BRAIN_STATE_DIR)
        
        if args.load:
            if trainer.load_state():
                logging.info("Loaded previous baby state")
            else:
                logging.info("No previous state found, starting fresh")
        
        logging.info(f"Starting training in {args.mode} mode...")
        await trainer.start_training(args.mode)
        
    except KeyboardInterrupt:
        logging.info("\nReceived shutdown signal. Saving brain state...")
        if trainer:
            trainer.save_state()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise
    finally:
        logging.info("Training session ended")

def run_main():
    """Entry point for the application"""
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    run_main()
