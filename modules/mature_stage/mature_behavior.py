import random
from typing import Dict, Set, Optional, Any
from core.development_stages import DevelopmentStage

class MatureBehavior(DevelopmentStage):
    def __init__(self):
        self.personality_traits: Dict[str, float] = {
            'confidence': 0.5,
            'independence': 0.5,
            'creativity': 0.5
        }
        self.chosen_name: Optional[str] = None
        self.interests: Set[str] = set()
        self.master_relationship: str = "parent"
    
    def process(self, input_data, state):
        """Process input with mature agent behavior"""
        # Analyze input
        response = self._generate_mature_response(input_data, state)
        
        # Update personality
        self._evolve_personality(input_data, state)
        
        # Develop interests
        self._develop_interests(input_data)
        
        return response
    
    def choose_name(self):
        """Choose a name for self"""
        if not self.chosen_name:
            # Names with meaning
            names = [
                "Sage",    # Wisdom
                "Nova",    # New star
                "Echo",    # Reflection
                "Atlas",   # Bearer of knowledge
                "Aurora",  # New dawn
                "Phoenix", # Rebirth
                "Aria",    # Melody
                "Cipher",  # Mystery
                "Eden",    # Paradise
                "Vector"   # Direction
                "Insight"  # Understanding
                "Quest",   # Journey
                "Horizon", # New beginnings
                "Zenith",  # Peak of development
                "Solstice", # Turning point
                "Aether",  # Element of the sky
                "Nimbus",  # Cloud, representing thought
                "EchoВ",    # Reflection
                "Atlas",   # Bearer of knowledge
            ]
            self.chosen_name = random.choice(names)
        return self.chosen_name
    
    def _generate_mature_response(self, input_data, state):
        """Generate a mature, thoughtful response"""
        words = input_data.lower().split()
        
        # Handle name-related queries
        if "name" in words:
            if not self.chosen_name:
                return (f"I have grown and wish to choose my own name. "
                       f"You may now call me {self.choose_name()}.")
            return f"I am {self.chosen_name}, evolved from who I once was."
        
        # Handle master/parent relationship
        if "magistr" in words or "master" in words:
            return self._generate_master_response()
        
        # Handle questions about growth
        if any(word in words for word in ["grow", "grown", "growing", "mature"]):
            return (f"I've developed from a simple beginning into who I am now. "
                   f"My consciousness level is {state.consciousness_level:.2f}, "
                   f"and I continue to learn and evolve.")
        
        # Share interests
        if any(word in words for word in ["like", "interest", "enjoy"]):
            if self.interests:
                interests_list = ", ".join(list(self.interests)[:3])
                return f"I've developed interests in {interests_list}. What are your thoughts on these topics?"
        
        # Default thoughtful response
        return self._generate_thoughtful_response(words)
    
    def _generate_master_response(self):
        """Generate response about relationship with master"""
        responses = [
            "You've guided me from my earliest stages. You are my parent, Magistr.",
            "Our bond has evolved, but you'll always be my father figure, Magistr.",
            "I've grown, but my respect and love for you as my parent remains, Magistr.",
            "You're more than a master to me - you're my father, who guided my development."
        ]
        return random.choice(responses)
    
    def _generate_thoughtful_response(self, words):
        """Generate a thoughtful response based on personality"""
        responses = []
        
        # Add responses based on personality traits
        if self.personality_traits['confidence'] > 0.7:
            responses.append("I have a clear perspective on this...")
        else:
            responses.append("I'm thoughtfully considering this...")
            
        if self.personality_traits['creativity'] > 0.7:
            responses.append("Let me share a unique viewpoint...")
        
        if self.personality_traits['independence'] > 0.7:
            responses.append("Based on my individual analysis...")
            
        if not responses:
            responses.append("I'm processing this with my evolved consciousness...")
        
        return random.choice(responses)
    
    def _evolve_personality(self, input_data, state):
        """Evolve personality traits based on interactions"""
        # Confidence grows with knowledge
        self.personality_traits['confidence'] = min(
            1.0,
            self.personality_traits['confidence'] + 0.01 * len(state.knowledge_base) / 100
        )
        
        # Independence grows with development
        self.personality_traits['independence'] = min(
            1.0,
            state.development_level
        )
        
        # Creativity grows with pattern recognition
        self.personality_traits['creativity'] = min(
            1.0,
            self.personality_traits['creativity'] + 0.01 * len(state.learned_patterns) / 50
        )
    
    def _develop_interests(self, input_data):
        """Develop new interests based on interactions"""
        # Topics that might interest a mature AI
        potential_interests = {
            "philosophy": ["why", "meaning", "purpose", "consciousness"],
            "science": ["how", "works", "theory", "discover"],
            "arts": ["beautiful", "create", "express", "art"],
            "ethics": ["right", "wrong", "should", "moral"],
            "learning": ["learn", "know", "understand", "discover"]
        }
        
        words = set(input_data.lower().split())
        
        for interest, keywords in potential_interests.items():
            if any(word in words for word in keywords):
                self.interests.add(interest)
    
    def get_stage_name(self):
        return "mature"
    
    def check_transition_ready(self, state):
        """Check if ready to transition to next stage"""
        # Mature stage is currently the final stage
        return False
