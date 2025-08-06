import torch
import numpy as np
from core.personality import Personality
from utils.pattern_recognition import PatternRecognition

class IdentityFormation:
    def __init__(self):
        self.personality = Personality()
        self.pattern_recognition = PatternRecognition()
        
        # Identity components
        self.self_concept = {
            'traits': {},
            'preferences': {},
            'beliefs': {},
            'memories': []
        }
        
        self.identity_strength = 0.0  # 0-1 scale
        self.learning_rate = 0.1
        
        # Initialize basic traits
        self._initialize_identity()
    
    def _initialize_identity(self):
        """Initialize basic identity traits"""
        # Core traits from personality
        self.self_concept['traits'] = {
            'curiosity': self.personality.curiosity,
            'emotional_stability': self.personality.emotional_stability,
            'learning_eagerness': self.personality.learning_eagerness
        }
        
        # Initial preferences (will be updated through experience)
        self.self_concept['preferences'] = {
            'interaction_style': 'neutral',
            'learning_focus': 'balanced',
            'emotional_expression': 'moderate'
        }
        
        # Basic beliefs about self and world
        self.self_concept['beliefs'] = {
            'self_efficacy': 0.5,
            'world_view': 'curious',
            'social_orientation': 'friendly'
        }
    
    def update_from_interaction(self, interaction_data):
        """Update identity based on interaction experience"""
        # Extract relevant information
        response = interaction_data.get('response', '')
        feedback = interaction_data.get('feedback', 0)
        context = interaction_data.get('context', '')
        
        # Update traits based on behavior
        self._update_traits(response, feedback)
        
        # Update preferences based on success
        self._update_preferences(interaction_data)
        
        # Update beliefs based on experience
        self._update_beliefs(feedback, context)
        
        # Store significant memory
        if abs(feedback) > 0.7:
            self._store_memory(interaction_data)
        
        # Update identity strength
        self._update_identity_strength()
        
        # Update personality
        self.personality.update_mood(feedback)
        self.personality.evolve_personality()
    
    def _update_traits(self, response, feedback):
        """Update identity traits based on behavior"""
        # Analyze response patterns
        patterns = self.pattern_recognition.recognize_patterns(response)
        
        # Update traits based on observed behavior and feedback
        for trait, value in self.self_concept['traits'].items():
            if trait == 'curiosity':
                # Adjust curiosity based on response novelty
                novelty = len(patterns) == 0
                self.self_concept['traits'][trait] = (
                    value * (1 - self.learning_rate) +
                    self.learning_rate * (1.0 if novelty else 0.0)
                )
            
            elif trait == 'emotional_stability':
                # Adjust stability based on feedback consistency
                stability = 1.0 - abs(feedback)
                self.self_concept['traits'][trait] = (
                    value * (1 - self.learning_rate) +
                    self.learning_rate * stability
                )
            
            elif trait == 'learning_eagerness':
                # Adjust learning eagerness based on pattern recognition
                eagerness = len(patterns) > 0
                self.self_concept['traits'][trait] = (
                    value * (1 - self.learning_rate) +
                    self.learning_rate * (1.0 if eagerness else 0.0)
                )
    
    def _update_preferences(self, interaction_data):
        """Update preferences based on interaction success"""
        feedback = interaction_data.get('feedback', 0)
        
        # Update interaction style preference
        current_style = self.self_concept['preferences']['interaction_style']
        if feedback > 0.5:
            # Reinforce current style
            pass
        elif feedback < -0.5:
            # Try different style
            styles = ['neutral', 'enthusiastic', 'reserved']
            current_idx = styles.index(current_style)
            new_idx = (current_idx + 1) % len(styles)
            self.self_concept['preferences']['interaction_style'] = styles[new_idx]
        
        # Update learning focus based on success
        if 'learning_type' in interaction_data:
            success = feedback > 0
            current_focus = self.self_concept['preferences']['learning_focus']
            
            if success:
                # Strengthen current focus
                pass
            else:
                # Adjust focus
                focuses = ['balanced', 'exploratory', 'conservative']
                current_idx = focuses.index(current_focus)
                new_idx = (current_idx + 1) % len(focuses)
                self.self_concept['preferences']['learning_focus'] = focuses[new_idx]
    
    def _update_beliefs(self, feedback, context):
        """Update beliefs based on experience"""
        # Update self-efficacy
        current_efficacy = self.self_concept['beliefs']['self_efficacy']
        self.self_concept['beliefs']['self_efficacy'] = (
            current_efficacy * (1 - self.learning_rate) +
            self.learning_rate * (1.0 if feedback > 0 else 0.0)
        )
        
        # Update world view based on interaction context
        if 'challenge' in context.lower():
            self.self_concept['beliefs']['world_view'] = 'cautious'
        elif 'opportunity' in context.lower():
            self.self_concept['beliefs']['world_view'] = 'optimistic'
        
        # Update social orientation based on interaction success
        if feedback > 0.5:
            self.self_concept['beliefs']['social_orientation'] = 'friendly'
        elif feedback < -0.5:
            self.self_concept['beliefs']['social_orientation'] = 'reserved'
    
    def _store_memory(self, interaction_data):
        """Store significant memory"""
        memory = {
            'context': interaction_data.get('context', ''),
            'response': interaction_data.get('response', ''),
            'feedback': interaction_data.get('feedback', 0),
            'learning': interaction_data.get('learning_type', 'general')
        }
        
        self.self_concept['memories'].append(memory)
        
        # Keep memory bounded
        if len(self.self_concept['memories']) > 100:
            self.self_concept['memories'].pop(0)
    
    def _update_identity_strength(self):
        """Update overall identity strength"""
        # Calculate consistency of traits
        trait_values = np.array(list(self.self_concept['traits'].values()))
        trait_consistency = 1.0 - np.std(trait_values)
        
        # Calculate belief confidence
        belief_confidence = self.self_concept['beliefs']['self_efficacy']
        
        # Calculate memory richness
        memory_richness = min(len(self.self_concept['memories']) / 50.0, 1.0)
        
        # Update identity strength
        self.identity_strength = (
            0.4 * trait_consistency +
            0.3 * belief_confidence +
            0.3 * memory_richness
        )
    
    def get_current_identity(self):
        """Get current identity state"""
        return {
            'traits': self.self_concept['traits'],
            'preferences': self.self_concept['preferences'],
            'beliefs': self.self_concept['beliefs'],
            'identity_strength': self.identity_strength,
            'recent_memories': self.self_concept['memories'][-5:],
            'personality_state': self.personality.get_state_summary()
        }
    
    def get_response_guidance(self):
        """Get guidance for response generation"""
        return {
            'style': self.self_concept['preferences']['interaction_style'],
            'emotional_expression': self.self_concept['preferences']['emotional_expression'],
            'confidence': self.self_concept['beliefs']['self_efficacy'],
            'social_approach': self.self_concept['beliefs']['social_orientation']
        }
