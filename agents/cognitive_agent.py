import torch
from pathlib import Path
from typing import Optional, Union
from core.brain_layers import BabyBrain
from core.memory_system import MemorySystem
from core.learning_engine import LearningEngine
from core.personality import Personality

class CognitiveAgent:
    def __init__(self, state_path: Optional[Union[str, Path]] = None):
        self.brain = BabyBrain()
        self.memory = MemorySystem()
        self.learning = LearningEngine(self.brain, self.memory)
        self.personality = Personality()
        
        # Load previous state if path provided
        if state_path:
            self.load_state(state_path)
    
    def load_state(self, state_path: str | Path) -> bool:
        """
        Load previous brain state from the specified path
        Returns True if successful, False otherwise
        """
        try:
            state_dict = torch.load(str(state_path))
            self.brain.load_state_dict(state_dict['brain'])
            self.personality = state_dict['personality']
            return True
        except Exception as e:
            print(f"Failed to load state: {e}")
            return False
    
    def save_state(self, state_path: Union[str, Path]) -> None:
        """Save current brain state to the specified path"""
        state_dict = {
            'brain': self.brain.state_dict(),
            'personality': self.personality
        }
        torch.save(state_dict, state_path)
    
    def process_input(self, input_text):
        """Process input and generate response"""
        # Update personality state
        self.personality.update_attention(len(input_text) / 1000)  # Proxy for complexity
        
        # Generate response
        with torch.no_grad():
            output = self.brain(input_text)
        
        # Process through personality filter
        response_style = self.personality.get_response_style()
        processed_output = self._apply_personality_style(output, response_style)
        
        # Learn from interaction
        self.learning.learn_from_batch([input_text])
        
        # Update energy levels
        self.personality.update_energy(0.1)  # Base energy cost for processing
        
        return processed_output
    
    def _apply_personality_style(self, output, style):
        """Apply personality style to raw output"""
        thoughts = output['thoughts']
        emotions = output['emotions']
        
        if style == "enthusiastic":
            confidence_boost = 1.2
            emotional_amplification = 1.3
        elif style == "reserved":
            confidence_boost = 0.8
            emotional_amplification = 0.7
        elif style == "tired":
            confidence_boost = 0.6
            emotional_amplification = 0.5
        elif style == "inquisitive":
            confidence_boost = 1.1
            emotional_amplification = 1.0
        else:  # neutral
            confidence_boost = 1.0
            emotional_amplification = 1.0
        
        output['thoughts'] *= confidence_boost
        output['emotions'] *= emotional_amplification
        
        return output
    
    def receive_feedback(self, feedback_score):
        """Process feedback and update personality"""
        self.personality.update_mood(feedback_score)
        
        if abs(feedback_score) > 0.5:  # Significant feedback
            self.learning.learn_from_feedback(
                self.memory.recall_short_term('last_input'),
                feedback_score
            )
        
        # Evolve personality based on accumulated experience
        if self.personality.learning_iterations % 100 == 0:
            self.personality.evolve_personality()
            self.save_state(Path('data/brain_state/latest.pth'))
    
    def get_personality_state(self):
        """Get current personality state"""
        return self.personality.get_state_summary()
    
    def rest(self):
        """Allow the agent to rest and recover energy"""
        recovery = 0.1
        self.personality.energy = min(1.0, self.personality.energy + recovery)
        
        # Process memories during rest
        recent_memories = self.memory.recall_by_type('experience', limit=5)
        for memory in recent_memories:
            # Strengthen important memories
            if memory['importance'] > 0.7:
                self.learning.learn_from_feedback(
                    memory['content']['input'],
                    memory['emotional_value']
                )
