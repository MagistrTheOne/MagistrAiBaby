"""
Reflection & Goal Generation: agents analyze past, set new goals.
"""
import random

class Reflection:
    def reflect(self, agent):
        # Analyze diary/memory for mistakes, set new goal
        if hasattr(agent, "diary") and agent.diary:
            mistakes = [d for d in agent.diary if d.get("emotions", {}).get("sadness", 0) > 0.7]
            if mistakes:
                agent.goal = "Избежать ошибок прошлого"
            else:
                agent.goal = random.choice(["Стать лидером", "Создать мем", "Помочь другу"])
            agent.memory.append(f"Рефлексия: {agent.goal}")
        else:
            agent.goal = "Исследовать мир"

REFLECTION = Reflection()
