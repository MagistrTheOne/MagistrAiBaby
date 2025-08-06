"""
Agent Modes: Parenting/learning modes for AI Magistr Baby NextGen Core.
"""

class AgentMode:
    CHAOTIC = "chaotic"
    LOVING = "loving"
    STRICT = "strict"

    @staticmethod
    def get_params(mode: str):
        if mode == AgentMode.CHAOTIC:
            return {"exploration": 1.0, "discipline": 0.1, "empathy": 0.2}
        if mode == AgentMode.LOVING:
            return {"exploration": 0.5, "discipline": 0.2, "empathy": 1.0}
        if mode == AgentMode.STRICT:
            return {"exploration": 0.2, "discipline": 1.0, "empathy": 0.3}
        return {"exploration": 0.5, "discipline": 0.5, "empathy": 0.5}
