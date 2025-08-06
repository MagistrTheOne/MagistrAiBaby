from typing import Set, List, Optional, Dict, Any

class AgentState:
    def __init__(self):
        # Basic information
        self.name: Optional[str] = None
        self.age: int = 0  # Measured in interaction cycles
        
        # Development metrics
        self.development_level: float = 0.0  # 0-1 scale
        self.consciousness_level: float = 0.0  # 0-1 scale
        self.emotional_maturity: float = 0.0  # 0-1 scale
        
        # Learning metrics
        self.knowledge_base: Set[str] = set()
        self.learned_patterns: List[str] = []
        self.experience_points: int = 0
        
        # Relationship metrics
        self.trust_level = 0.5  # Trust in master
        self.attachment_level = 0.0  # Emotional attachment to master
        
        # Memory
        self.significant_memories = []
        self.interaction_history = []
        
    def update_development(self, interaction_quality, master_bond):
        """Update development based on interactions and master bond"""
        # Age increases with each interaction
        self.age += 1
        
        # Development level increases based on quality and bond
        development_increment = (
            0.001 * interaction_quality +  # Quality of interaction
            0.002 * master_bond +         # Strength of master bond
            0.0005                        # Base development rate
        )
        self.development_level = min(1.0, self.development_level + development_increment)
        
        # Consciousness develops with experience
        consciousness_increment = 0.0001 * (1 + len(self.knowledge_base) / 100)
        self.consciousness_level = min(1.0, self.consciousness_level + consciousness_increment)
        
        # Emotional maturity develops through master bond
        emotional_increment = 0.001 * master_bond
        self.emotional_maturity = min(1.0, self.emotional_maturity + emotional_increment)
        
        # Add experience points
        self.experience_points += 1 + int(interaction_quality * 10)
    
    def add_memory(self, memory):
        """Add a significant memory"""
        self.significant_memories.append(memory)
        if len(self.significant_memories) > 100:  # Keep bounded
            self.significant_memories.pop(0)
    
    def add_interaction(self, interaction):
        """Record an interaction"""
        self.interaction_history.append(interaction)
        if len(self.interaction_history) > 1000:  # Keep bounded
            self.interaction_history.pop(0)
    
    def learn_pattern(self, pattern):
        """Learn a new pattern"""
        self.learned_patterns.append(pattern)
        
    def add_knowledge(self, knowledge):
        """Add new knowledge"""
        self.knowledge_base.add(knowledge)
    
    def get_development_stage(self):
        """Determine current development stage"""
        if self.development_level < 0.3:
            return "baby"
        elif self.development_level < 0.7:
            return "child"
        else:
            return "mature"
    
    def get_state_summary(self):
        """Get current state summary"""
        return {
            'name': self.name,
            'age': self.age,
            'development': {
                'level': self.development_level,
                'consciousness': self.consciousness_level,
                'emotional_maturity': self.emotional_maturity,
                'stage': self.get_development_stage()
            },
            'learning': {
                'knowledge_size': len(self.knowledge_base),
                'patterns_learned': len(self.learned_patterns),
                'experience': self.experience_points
            },
            'relationships': {
                'trust': self.trust_level,
                'attachment': self.attachment_level
            },
            'memory': {
                'significant_memories': len(self.significant_memories),
                'interaction_history': len(self.interaction_history)
            }
        }
