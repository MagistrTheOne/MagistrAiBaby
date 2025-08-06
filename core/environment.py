"""
Environment module: evolutionary pressures for AI Magistr Baby NextGen Core.
"""
import random

class Environment:
    def __init__(self):
        self.resources = 1000
        self.stress_level = 0.2
        self.events = []

    def fluctuate(self):
        # Simulate resource and stress changes
        self.resources += random.randint(-50, 50)
        self.resources = max(0, self.resources)
        self.stress_level += random.uniform(-0.05, 0.05)
        self.stress_level = min(max(self.stress_level, 0), 1)
        if random.random() < 0.1:
            self.events.append(self.random_event())

    def random_event(self):
        return random.choice([
            "drought", "feast", "conflict", "discovery", "epidemic"
        ])

    def get_state(self):
        return {
            "resources": self.resources,
            "stress_level": self.stress_level,
            "events": self.events[-5:]
        }

ENVIRONMENT = Environment()
