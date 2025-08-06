"""
CultureManager: управление коллективной памятью, мемами и культурной динамикой среди агентов.
"""
import time
from typing import List, Dict
from .meme import Meme

class CultureManager:
    def __init__(self):
        self.memes: List[Meme] = []
        self.generation = 0

    def add_meme(self, meme: Meme):
        self.memes.append(meme)

    def spread_meme(self, meme: Meme, agent_id: str):
        meme.spread(agent_id, time.time())

    def decay_memes(self):
        for meme in self.memes:
            meme.decay()
        # Удаляем забытые мемы
        self.memes = [m for m in self.memes if m.popularity > 0.1]

    def trending_memes(self) -> List[Meme]:
        return [m for m in self.memes if m.is_trending()]

    def get_culture_snapshot(self) -> List[Dict]:
        return [m.to_dict() for m in self.memes]
