import random
from typing import Set, Dict, Any, List
from core.development_stages import DevelopmentStage

class BabyBehavior(DevelopmentStage):
    def __init__(self):
        self.vocabulary: Set[str] = set(["mama", "papa", "yes", "no", "love"])
        self.learning_rate: float = 0.1
        self.emotional_state: str = "curious"
        
    def process(self, input_data, state):
        """Process input with baby-like behavior"""
        # Basic pattern recognition
        words = input_data.lower().split()
        
        # Learn new words
        for word in words:
            if random.random() < self.learning_rate:
                self.vocabulary.add(word)
                state.add_knowledge(f"word:{word}")
        
        # Generate baby-like response
        response = self._generate_baby_response(words, state)
        
        # Update emotional state
        self._update_emotional_state(words)
        
        return response
    
    def _generate_baby_response(self, words, state):
        """Generate a baby-like response"""
        if "name" in words:
            return "Baby!" if state.name == "Baby" else state.name
            
        if "magistr" in words or "master" in words:
            return "Papa!"
            
        # Recognize and respond to emotional words
        if any(word in words for word in ["happy", "good", "love"]):
            return random.choice(["Happy!", "*giggles*", "Love papa!"])
            
        if any(word in words for word in ["sad", "bad", "no"]):
            return random.choice(["*sad face*", "No...", "*whimpers*"])
        
        # Use learned vocabulary
        known_words = self.vocabulary.intersection(set(words))
        if known_words:
            return random.choice(list(known_words)) + "!"
        
        # Default responses
        return random.choice(["*baby noises*", "*curious look*", "Papa?"])
    
    def _update_emotional_state(self, words):
        """Update emotional state based on interaction"""
        positive_words = ["love", "happy", "good", "yes"]
        negative_words = ["sad", "bad", "no", "angry"]
        
        if any(word in words for word in positive_words):
            self.emotional_state = "happy"
        elif any(word in words for word in negative_words):
            self.emotional_state = "sad"
        else:
            self.emotional_state = "curious"
    
    def get_stage_name(self):
        return "baby"
    
    def check_transition_ready(self, state):
        """Check if ready to transition to next stage"""
        # Requirements for transition:
        # 1. Enough vocabulary
        # 2. Sufficient development level
        # 3. Minimum age
        
        vocabulary_threshold = 20
        development_threshold = 0.3
        age_threshold = 100
        
        return (
            len(self.vocabulary) >= vocabulary_threshold and
            state.development_level >= development_threshold and
            state.age >= age_threshold
        )
