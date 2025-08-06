"""
FastAPI/WebSocket API для наблюдения и управления мультиагентной средой AI Magistr Baby V2 NextGenAlpha в реальном времени.
"""
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from core.nextgen_world import AIBabyWorld
import uvicorn

app = FastAPI()
world = AIBabyWorld(num_agents=8)

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
