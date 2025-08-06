"""
NextGen мультиагентная среда для AI Magistr Baby V2 NextGenAlpha.
Агенты учатся, общаются, эволюционируют и формируют цифровую культуру.
"""
import random
import time
from typing import List, Dict, Any, Optional
from core.culture.culture_manager import CultureManager
from core.culture.meme import Meme

class AIBabyAgent:
    def __init__(self, agent_id: str, generation: int = 0, parent_id: Optional[str] = None):
        self.agent_id = agent_id
        self.generation = generation
        self.parent_id = parent_id
        self.memory: List[str] = []
        self.skills: Dict[str, float] = {}
        self.emotions: Dict[str, float] = {'joy': 0.5, 'sadness': 0.5}
        self.diary: List[Dict[str, Any]] = []
        self.culture: List[Meme] = []
        self.rules: List[str] = []
        self.alive = True
        self.age = 0

    def perceive(self, message: str, meme: Optional[Meme] = None):
        self.memory.append(message)
        if meme:
            self.culture.append(meme)

    def act(self, world: 'AIBabyWorld'):
        # Пример: иногда агент генерирует новый мем или правило
        if random.random() < 0.1:
            meme = Meme(content=f"Мем от {self.agent_id} #{random.randint(1,1000)}", author_id=self.agent_id)
            world.culture_manager.add_meme(meme)
        if random.random() < 0.05:
            rule = f"Новое правило от {self.agent_id}: не перебивать старших!"
            world.add_rule(rule)
        # Эмоции и самоанализ
        self.emotions['joy'] = min(1.0, self.emotions['joy'] + random.uniform(-0.05, 0.05))
        self.emotions['sadness'] = min(1.0, self.emotions['sadness'] + random.uniform(-0.05, 0.05))
        self.diary.append({'age': self.age, 'emotions': self.emotions.copy(), 'memory': len(self.memory)})
        self.age += 1
        # Передача опыта младшим (если есть)
        if self.generation > 0 and random.random() < 0.05:
            world.inherit_experience(self)

    def interact(self, other: 'AIBabyAgent', world: 'AIBabyWorld'):
        # Обмен мемами и эмоциями
        if world.culture_manager.memes:
            meme = random.choice(world.culture_manager.memes)
            other.perceive(f"{self.agent_id} делится мемом", meme)
        # Эмоциональный обмен
        other.emotions['joy'] = (other.emotions['joy'] + self.emotions['joy']) / 2

    def evolve(self):
        # Пример: если агент слишком "грустный" — исчезает
        if self.emotions['sadness'] > 0.95:
            self.alive = False

class AIBabyWorld:
    def __init__(self, num_agents: int = 5):
        self.culture_manager = CultureManager()
        self.agents: List[AIBabyAgent] = [AIBabyAgent(f"agent_{i}") for i in range(num_agents)]
        self.rules: List[str] = []
        self.generation = 0

    def add_rule(self, rule: str):
        self.rules.append(rule)

    def inherit_experience(self, parent: AIBabyAgent):
        # Создать нового агента с частью памяти и культуры родителя
        new_id = f"agent_{len(self.agents)}"
        child = AIBabyAgent(new_id, generation=parent.generation+1, parent_id=parent.agent_id)
        child.memory = parent.memory[-5:]
        child.culture = parent.culture[-2:]
        self.agents.append(child)

    def step(self):
        # Каждый агент действует и взаимодействует
        for agent in self.agents:
            if agent.alive:
                agent.act(self)
        # Случайные взаимодействия
        for _ in range(len(self.agents)):
            a, b = random.sample(self.agents, 2)
            if a.alive and b.alive:
                a.interact(b, self)
        # Культурная динамика
        self.culture_manager.decay_memes()
        # Эволюция: удаляем неадаптивных
        self.agents = [a for a in self.agents if a.alive]

    def snapshot(self) -> dict:
        return {
            'num_agents': len(self.agents),
            'rules': self.rules,
            'culture': self.culture_manager.get_culture_snapshot(),
            'agents': [a.agent_id for a in self.agents]
        }
