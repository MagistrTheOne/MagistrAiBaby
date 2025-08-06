from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from core.agent_state import AgentState

class DevelopmentStage(ABC):
    @abstractmethod
    def process(self, input_data: str, state: "AgentState") -> str:
        """Process input based on current development stage"""
        raise NotImplementedError
    
    @abstractmethod
    def get_stage_name(self) -> str:
        """Get the name of this development stage"""
        pass
    
    @abstractmethod
    def check_transition_ready(self, state: Any) -> bool:
        """Check if ready to transition to next stage"""
        pass
