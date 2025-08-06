"""
Модуль для представления и распространения "мемов" (идей, привычек, паттернов) среди агентов.
"""
import random
from typing import List, Dict, Any

class Meme:
    """Базовый класс для культурного паттерна (мема)."""
    def __init__(self, content: str, author_id: str, tags: List[str] = None):
        self.content = content
        self.author_id = author_id
        self.tags = tags or []
        self.popularity = 1.0  # Базовая популярность
        self.history = []  # Список (agent_id, timestamp)

    def spread(self, agent_id: str, timestamp: float):
        """Агент распространяет мем — увеличивается популярность и история."""
        self.popularity *= 1.05 + random.uniform(-0.01, 0.01)
        self.history.append((agent_id, timestamp))

    def decay(self):
        """Постепенное забывание мема."""
        self.popularity *= 0.99

    def is_trending(self) -> bool:
        return self.popularity > 1.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            'content': self.content,
            'author_id': self.author_id,
            'tags': self.tags,
            'popularity': self.popularity,
            'history': self.history
        }
