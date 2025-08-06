"""
Emotional Memory System: Groq-accelerated memory with emotional context, decay, importance, and association.
"""
from typing import Any, Dict
from .groq_accelerator import GROQ_ACCELERATOR
import time

class EmotionalMemory:
    def __init__(self):
        self.memories = []  # List of dicts: {event, emotion, timestamp, importance}

    def remember(self, event: str, emotion: str, importance: float = 1.0):
        self.memories.append({
            "event": event,
            "emotion": emotion,
            "timestamp": time.time(),
            "importance": importance
        })

    def decay(self):
        now = time.time()
        self.memories = [m for m in self.memories if (now - m["timestamp"]) < 86400 or m["importance"] > 0.5]

    def associate(self, cue: str) -> Any:
        """Find associated memory using Groq acceleration."""
        return GROQ_ACCELERATOR.associate_memory({"cue": cue, "memories": self.memories})

    def emotional_state(self) -> Dict[str, float]:
        """Aggregate current emotional state using Groq acceleration."""
        return GROQ_ACCELERATOR.aggregate_emotion({"memories": self.memories})

EMOTIONAL_MEMORY = EmotionalMemory()
