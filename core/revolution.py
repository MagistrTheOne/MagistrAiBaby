"""
Revolution module: meme revolutions and global rule changes.
"""
class Revolution:
    def check_revolution(self, world):
        # If a meme is in >60% of agents, trigger revolution
        meme_counts = {}
        for agent in world.agents:
            for meme in getattr(agent, "culture", []):
                key = meme.content if hasattr(meme, "content") else str(meme)
                meme_counts[key] = meme_counts.get(key, 0) + 1
        for meme, count in meme_counts.items():
            if count / max(1, len(world.agents)) > 0.6:
                world.add_rule(f"Революция: {meme}")
                return meme
        return None

REVOLUTION = Revolution()
