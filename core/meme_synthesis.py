"""
Meme Synthesis: hybrid meme generation when agents interact.
"""
import random
from core.culture.meme import Meme

class MemeSynthesis:
    def synthesize(self, meme1, meme2, agent1, agent2):
        # Combine content, tags, and authors
        content = f"{meme1.content[:10]}...+{meme2.content[:10]}..."
        tags = list(set(meme1.tags + meme2.tags))
        author_id = f"{agent1.agent_id}&{agent2.agent_id}"
        return Meme(content=content, author_id=author_id, tags=tags)

MEME_SYNTHESIS = MemeSynthesis()
