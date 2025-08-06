"""
AgentSociety: управление популяцией агентов, их связями и культурной эволюцией.
"""
from typing import List, Dict
from .culture_manager import CultureManager

class AgentSociety:
    def __init__(self, agent_ids: List[str]):
        self.agent_ids = agent_ids
        self.culture = CultureManager()
        self.relationships: Dict[str, Dict[str, float]] = {aid: {} for aid in agent_ids}

    def interact(self, agent_a: str, agent_b: str, meme_content: str):
        """Агенты обмениваются мемом и укрепляют связь."""
        meme = self.culture.trending_memes()[0] if self.culture.trending_memes() else None
        if meme:
            self.culture.spread_meme(meme, agent_b)
        else:
            meme = self.culture.add_meme(meme_content)
        self._strengthen_relationship(agent_a, agent_b)

    def _strengthen_relationship(self, a: str, b: str):
        self.relationships[a][b] = self.relationships[a].get(b, 0.0) + 0.1
        self.relationships[b][a] = self.relationships[b].get(a, 0.0) + 0.1

    def decay_relationships(self):
        for a in self.relationships:
            for b in self.relationships[a]:
                self.relationships[a][b] *= 0.99
