"""
Скрипт запуска симуляции мультиагентной среды AI Magistr Baby V2 NextGenAlpha.
"""
import time
from core.nextgen_world import AIBabyWorld

if __name__ == "__main__":
    world = AIBabyWorld(num_agents=8)
    steps = 100
    for step in range(steps):
        world.step()
        if step % 10 == 0:
            snap = world.snapshot()
            print(f"Step {step}: {snap['num_agents']} agents, {len(snap['culture'])} memes, rules: {len(snap['rules'])}")
            print(f"  Agents: {snap['agents']}")
            print(f"  Trending memes: {[m['content'] for m in snap['culture'] if m['popularity'] > 1.5]}")
            print(f"  Rules: {snap['rules']}")
        time.sleep(0.1)
    print("--- Simulation finished ---")
    print(f"Final snapshot: {world.snapshot()}")
