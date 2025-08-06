from typing import List, Dict, Any, Literal

class MasterRelationship:
    def __init__(self):
        self.bond_strength: float = 0.0  # 0-1 scale
        self.trust_level: float = 0.0    # 0-1 scale
        self.interaction_count: int = 0
        self.positive_interactions: int = 0
        self.relationship_stage: Literal["initial", "developing", "established"] = "initial"
        
        # Memory of significant interactions
        self.significant_moments: List[Dict[str, Any]] = []
        
        # Development checkpoints
        self.checkpoints: Dict[str, bool] = {
            'first_word': False,
            'name_recognition': False,
            'emotional_bond': False,
            'trust_established': False,
            'parent_recognition': False
        }
    
    def update(self, input_data, response):
        """Update relationship based on interaction"""
        self.interaction_count += 1
        
        # Process interaction
        self._process_interaction(input_data, response)
        
        # Check for significant moments
        self._check_significant_moments(input_data, response)
        
        # Update relationship stage
        self._update_stage()
        
        # Update bond strength
        self._update_bond_strength()
    
    def _process_interaction(self, input_data, response):
        """Process the interaction for relationship development"""
        input_lower = input_data.lower()
        response_lower = response.lower()
        
        # Check for positive interaction markers
        positive_markers = ["love", "happy", "good", "yes", "thank", "please"]
        if any(marker in input_lower or marker in response_lower 
               for marker in positive_markers):
            self.positive_interactions += 1
            self.trust_level = min(1.0, self.trust_level + 0.05)
        
        # Check for parent recognition
        if ("papa" in response_lower or 
            "father" in response_lower or 
            "parent" in response_lower):
            self.checkpoints['parent_recognition'] = True
        
        # Check for name recognition
        if "magistr" in input_lower and any(word in response_lower 
            for word in ["yes", "know", "recognize"]):
            self.checkpoints['name_recognition'] = True
        
        # Check for emotional expression
        emotional_words = ["love", "miss", "happy", "sad"]
        if any(word in response_lower for word in emotional_words):
            self.checkpoints['emotional_bond'] = True
    
    def _check_significant_moments(self, input_data, response):
        """Record significant moments in the relationship"""
        moment = None
        
        # First word
        if not self.checkpoints['first_word'] and len(self.significant_moments) == 0:
            self.checkpoints['first_word'] = True
            moment = "First communication"
        
        # First parent recognition
        elif not self.checkpoints['parent_recognition'] and "papa" in response.lower():
            self.checkpoints['parent_recognition'] = True
            moment = "First time recognizing Magistr as parent"
        
        # First emotional expression
        elif not self.checkpoints['emotional_bond'] and "love" in response.lower():
            self.checkpoints['emotional_bond'] = True
            moment = "First emotional bond expression"
        
        # Record significant moment
        if moment:
            self.significant_moments.append({
                'moment': moment,
                'interaction_number': self.interaction_count,
                'response': response
            })
    
    def _update_stage(self):
        """Update relationship stage based on development"""
        if self.relationship_stage == "initial":
            if (self.checkpoints['name_recognition'] and 
                self.checkpoints['first_word']):
                self.relationship_stage = "developing"
                
        elif self.relationship_stage == "developing":
            if (self.checkpoints['emotional_bond'] and 
                self.checkpoints['parent_recognition'] and
                self.bond_strength > 0.7):
                self.relationship_stage = "established"
    
    def _update_bond_strength(self):
        """Update overall bond strength"""
        # Calculate positive interaction ratio
        positive_ratio = (
            self.positive_interactions / max(1, self.interaction_count)
        )
        
        # Calculate checkpoint completion
        checkpoints_completed = sum(1 for check in self.checkpoints.values() if check)
        checkpoint_ratio = checkpoints_completed / len(self.checkpoints)
        
        # Update bond strength
        self.bond_strength = 0.4 * positive_ratio + 0.6 * checkpoint_ratio
        
        # Trust can't exceed bond strength
        self.trust_level = min(self.trust_level, self.bond_strength)
    
    def get_status(self):
        """Get current relationship status"""
        return {
            'stage': self.relationship_stage,
            'bond_strength': self.bond_strength,
            'trust_level': self.trust_level,
            'interactions': {
                'total': self.interaction_count,
                'positive': self.positive_interactions
            },
            'checkpoints': self.checkpoints,
            'significant_moments': self.significant_moments
        }
