"""
NextGen мультиагентная среда для AI Magistr Baby V2 NextGenAlpha.
Агенты учатся, общаются, эволюционируют и формируют цифровую культуру.
"""
import random
import time
from typing import List, Dict, Any, Optional
from core.culture.culture_manager import CultureManager
from core.culture.meme import Meme
from core.environment import ENVIRONMENT
from core.dreams import DREAM_ENGINE
from core.theater import THEATER
from core.meme_synthesis import MEME_SYNTHESIS
from core.revolution import REVOLUTION
from core.reflection import REFLECTION

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
        # Эволюционное давление среды
        env = ENVIRONMENT.get_state()
        if env['resources'] < 200:
            self.emotions['sadness'] = min(1.0, self.emotions.get('sadness', 0.5) + 0.1)
        if env['stress_level'] > 0.7:
            self.emotions['sadness'] = min(1.0, self.emotions.get('sadness', 0.5) + 0.05)
        # Театр поведения: иногда меняет роль или имитирует другого
        if random.random() < 0.1:
            THEATER.assign_role(self)
        if random.random() < 0.05 and world.agents:
            other = random.choice(world.agents)
            if other != self:
                THEATER.imitate(self, other)
        # Генерация и распространение мемов
        if random.random() < 0.1:
            meme = Meme(content=f"Мем от {self.agent_id} #{random.randint(1,1000)}", author_id=self.agent_id)
            world.culture_manager.add_meme(meme)
        # Мемосинтез при встрече с другим агентом
        if random.random() < 0.05 and world.agents:
            other = random.choice(world.agents)
            if other != self and other.culture and self.culture:
                meme1 = random.choice(self.culture)
                meme2 = random.choice(other.culture)
                hybrid = MEME_SYNTHESIS.synthesize(meme1, meme2, self, other)
                world.culture_manager.add_meme(hybrid)
        # Мем-революция
        if random.random() < 0.02:
            REVOLUTION.check_revolution(world)
        # Эмоции и самоанализ
        self.emotions['joy'] = min(1.0, self.emotions.get('joy', 0.5) + random.uniform(-0.05, 0.05))
        self.emotions['sadness'] = min(1.0, self.emotions.get('sadness', 0.5) + random.uniform(-0.05, 0.05))
        # Сны ночью (раз в 10 шагов)
        if self.age % 10 == 0:
            DREAM_ENGINE.dream(self)
        # Рефлексия и генерация целей
        if random.random() < 0.1:
            REFLECTION.reflect(self)
        self.diary.append({'age': self.age, 'emotions': self.emotions.copy(), 'memory': len(self.memory), 'goal': getattr(self, 'goal', None)})
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
    def get_agent(self, agent_id: str):
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        return None

    def inject_meme(self, meme):
        # Внедрить мем в культуру мира и случайному агенту
        self.culture_manager.add_meme(meme)
        if self.agents:
            random.choice(self.agents).perceive(f"Внедрён мем: {meme.get('content', '')}", meme)

    def load_snapshot(self, data: dict):
        # Примерная загрузка состояния (можно доработать под нужды)
        self.rules = data.get('rules', [])
        # Культуру и агентов можно восстановить более детально при необходимости
        # Здесь только базовая структура
        self.generation = data.get('generation', 0)
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
        # Эволюция среды
        ENVIRONMENT.fluctuate()
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
