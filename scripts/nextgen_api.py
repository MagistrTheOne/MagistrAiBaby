from core.environment import ENVIRONMENT
@app.get("/environment")
def get_environment():
    """Получить состояние среды (ресурсы, стресс, события)."""
    return ENVIRONMENT.get_state()
"""
FastAPI/WebSocket API для наблюдения и управления мультиагентной средой AI Magistr Baby V2 NextGenAlpha в реальном времени.
"""
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from core.nextgen_world import AIBabyWorld
from core.meme_engine import MEME_ENGINE
from utils.memory import EMOTIONAL_MEMORY
from core.agent_modes import AgentMode
import json
import uvicorn


app = FastAPI()
world = AIBabyWorld(num_agents=8)
@app.post("/inject_meme")
def inject_meme(payload: dict):
    """Внедрить мем в культуру/агента."""
    meme = MEME_ENGINE.generate_meme(payload)
    world.inject_meme(meme)
    return {"status": "ok", "meme": meme}

@app.post("/trigger_emotion")
def trigger_emotion(payload: dict):
    """Запустить эмоциональное событие для агента."""
    agent_id = payload.get("agent_id")
    event = payload.get("event")
    emotion = payload.get("emotion")
    importance = payload.get("importance", 1.0)
    agent = world.get_agent(agent_id)
    if agent:
        agent.memory.remember(event, emotion, importance)
        return {"status": "ok"}
    return {"status": "error", "reason": "agent not found"}

@app.post("/evolve_agent")
def evolve_agent(payload: dict):
    """Развить агента с учетом режима воспитания."""
    agent_id = payload.get("agent_id")
    mode = payload.get("mode", AgentMode.LOVING)
    params = AgentMode.get_params(mode)
    agent = world.get_agent(agent_id)
    if agent:
        agent.evolve(params)
        return {"status": "ok", "params": params}
    return {"status": "error", "reason": "agent not found"}

@app.post("/save")
def save():
    """Сохранить состояние мира."""
    with open("world_save.json", "w", encoding="utf-8") as f:
        json.dump(world.snapshot(), f, ensure_ascii=False, indent=2)
    return {"status": "ok"}

@app.post("/load")
def load():
    """Загрузить состояние мира."""
    try:
        with open("world_save.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        world.load_snapshot(data)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "reason": str(e)}

@app.get("/snapshot")
def get_snapshot():
    """Получить текущее состояние мира."""
    return JSONResponse(world.snapshot())

@app.post("/step")
def step():
    """Сделать один шаг эволюции."""
    world.step()
    return JSONResponse(world.snapshot())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            world.step()
            await websocket.send_json(world.snapshot())
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    uvicorn.run("scripts.nextgen_api:app", host="0.0.0.0", port=8000, reload=True)
