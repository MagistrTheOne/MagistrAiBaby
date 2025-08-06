"""
Theater module: behavioral masks, imitation, and role play for agents.
"""
import random

class Theater:
    ROLES = ["leader", "joker", "outcast", "sage", "follower"]

    def assign_role(self, agent):
        agent.role = random.choice(self.ROLES)

    def imitate(self, agent, other):
        # Agent imitates another's emotions/behavior
        for k in other.emotions:
            agent.emotions[k] = (agent.emotions.get(k, 0.5) + other.emotions[k]) / 2
        agent.memory.append(f"Имитировал {other.agent_id}")

THEATER = Theater()
