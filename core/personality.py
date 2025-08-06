from config.settings import (
    INITIAL_CURIOSITY,
    EMOTIONAL_STABILITY,
    LEARNING_EAGERNESS
)

class Personality:
    def __init__(self):
        # Core traits (0-1 scale)
        self.curiosity = INITIAL_CURIOSITY
        self.emotional_stability = EMOTIONAL_STABILITY
        self.learning_eagerness = LEARNING_EAGERNESS
        
        # Dynamic states
        self.mood = 0.5  # -1 to 1 scale
        self.energy = 1.0  # 0-1 scale
        self.attention_span = 0.8  # 0-1 scale
        
        # Experience counters
        self.positive_experiences = 0
        self.negative_experiences = 0
        self.learning_iterations = 0
    
    def update_mood(self, emotional_value):
        """Update mood based on emotional experience"""
        # Mood changes more slowly when emotional stability is high
        impact = (1 - self.emotional_stability) * emotional_value
        self.mood = max(-1, min(1, self.mood + impact))
        
        if emotional_value > 0:
            self.positive_experiences += 1
        else:
            self.negative_experiences += 1
    
    def update_energy(self, activity_intensity):
        """Update energy levels based on activity"""
        energy_cost = activity_intensity * (1 - self.learning_eagerness)
        self.energy = max(0.1, min(1.0, self.energy - energy_cost))
    
    def update_attention(self, task_complexity):
        """Update attention span based on task complexity"""
        attention_change = (task_complexity - 0.5) * self.curiosity
        self.attention_span = max(0.2, min(1.0, self.attention_span + attention_change))
    
    def get_learning_motivation(self):
        """Calculate current learning motivation"""
        base_motivation = self.learning_eagerness
        mood_factor = (self.mood + 1) / 2  # Convert -1:1 to 0:1
        energy_factor = self.energy
        attention_factor = self.attention_span
        
        motivation = (
            0.4 * base_motivation +
            0.2 * mood_factor +
            0.2 * energy_factor +
            0.2 * attention_factor
        )
        
        return motivation
    
    def get_response_style(self):
        """Determine current response style based on personality state"""
        if self.mood > 0.5:
            style = "enthusiastic"
        elif self.mood < -0.5:
            style = "reserved"
        else:
            style = "neutral"
            
        if self.energy < 0.3:
            style = "tired"
        elif self.curiosity > 0.8 and self.attention_span > 0.7:
            style = "inquisitive"
            
        return style
    
    def evolve_personality(self):
        """Evolve personality traits based on accumulated experience"""
        # Adjust curiosity based on learning success
        experience_ratio = (
            self.positive_experiences /
            max(1, self.positive_experiences + self.negative_experiences)
        )
        
        self.curiosity = max(0.1, min(1.0,
            self.curiosity + (experience_ratio - 0.5) * 0.1
        ))
        
        # Adjust emotional stability based on mood volatility
        if abs(self.mood) < 0.3:  # Stable mood
            self.emotional_stability = min(1.0, self.emotional_stability + 0.05)
        else:  # Volatile mood
            self.emotional_stability = max(0.1, self.emotional_stability - 0.05)
        
        # Adjust learning eagerness based on motivation trends
        motivation = self.get_learning_motivation()
        if motivation > 0.7:
            self.learning_eagerness = min(1.0, self.learning_eagerness + 0.05)
        elif motivation < 0.3:
            self.learning_eagerness = max(0.1, self.learning_eagerness - 0.05)
        
        self.learning_iterations += 1
    
    def get_state_summary(self):
        """Get current personality state summary"""
        return {
            'traits': {
                'curiosity': self.curiosity,
                'emotional_stability': self.emotional_stability,
                'learning_eagerness': self.learning_eagerness
            },
            'states': {
                'mood': self.mood,
                'energy': self.energy,
                'attention_span': self.attention_span
            },
            'experience': {
                'positive': self.positive_experiences,
                'negative': self.negative_experiences,
                'learning_iterations': self.learning_iterations
            }
        }
