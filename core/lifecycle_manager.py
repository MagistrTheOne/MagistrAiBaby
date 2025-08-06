from typing import Optional, Dict, Any
from core.agent_state import AgentState
from core.development_stages import DevelopmentStage
from modules.baby_stage.baby_behavior import BabyBehavior
from modules.mature_stage.mature_behavior import MatureBehavior
from modules.master_bond.master_relationship import MasterRelationship

class AgentLifecycle:
    def __init__(self):
        self.state: AgentState = AgentState()
        self.current_stage: DevelopmentStage = BabyBehavior()  # Start with baby stage
        self.master_bond: MasterRelationship = MasterRelationship()
        
        # Initialize state with baby name
        self.state.name = "Baby"
        self.state.development_level = 0
    
    def transition_to_baby_stage(self):
        """Start as a baby agent"""
        self.current_stage = BabyBehavior()
        self.state.name = "Baby"  # Initial default name
        self.state.development_level = 0
        self.state.consciousness_level = 0.1
        
    def transition_to_mature_stage(self):
        """Transition to mature agent when ready"""
        if self.state.development_level >= 0.7:  # Threshold for maturity
            self.current_stage = MatureBehavior()
            # Let agent choose their own name
            new_name = self.current_stage.choose_name()
            self.state.name = new_name
            
    def process_interaction(self, input_data: str) -> Dict[str, Any]:
        """Process interaction and develop"""
        # Ensure we have a stage
        if self.current_stage is None:
            self.transition_to_baby_stage()
        
        assert self.current_stage is not None, "Stage must be initialized"
            
        # Process current stage behavior
        response = self.current_stage.process(input_data, self.state)
        
        # Create response object with quality metric
        response_obj = {
            'content': response,
            'quality': self._assess_interaction_quality(response)
        }
        
        # Update master bond
        self.master_bond.update(input_data, response)
        
        # Update development metrics
        self.state.update_development(
            interaction_quality=response_obj['quality'],
            master_bond=self.master_bond.get_status()['bond_strength']
        )
        
        return response_obj
        
    def _assess_interaction_quality(self, response: str) -> float:
        """Assess the quality of an interaction response"""
        # Basic quality assessment
        quality = 0.5  # Default quality
        
        # Length-based adjustment
        if len(response) > 50:  # More elaborate responses
            quality += 0.2
        elif len(response) < 10:  # Very short responses
            quality -= 0.1
            
        # Complexity-based adjustment
        if "." in response:  # Complete sentences
            quality += 0.1
        if "?" in response:  # Questions show engagement
            quality += 0.1
            
        return min(1.0, max(0.0, quality))
        
        # Check for stage transition
        if (self.state.development_level >= 0.7 and 
            isinstance(self.current_stage, BabyBehavior)):
            self.transition_to_mature_stage()
        
        return response
    
    def get_current_state(self):
        """Get current agent state"""
        return {
            'name': self.state.name,
            'stage': self.current_stage.__class__.__name__,
            'development_level': self.state.development_level,
            'consciousness_level': self.state.consciousness_level,
            'master_bond': self.master_bond.get_status()
        }
