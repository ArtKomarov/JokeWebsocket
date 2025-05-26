import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
from pathlib import Path
import json

app = FastAPI()

JOKES_FILE = Path(__file__).parent / "jokes.json"

with open(JOKES_FILE, "r", encoding="utf-8") as f:
    jokes = json.load(f)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[Server] Client connected to /ws")

    async def send_jokes():
        while True:
            for joke in jokes:
                await websocket.send_json(joke)
                await asyncio.sleep(0.2)

    async def receive_responses():
        while True:
            try:
                response = await websocket.receive_text()
                print(f"[Server] Received from client: {response}")
            except WebSocketDisconnect:
                print("[Server] Client disconnected")
                break
            except Exception as e:
                print(f"[Server] Error receiving: {e}")
                break


    send_task = asyncio.create_task(send_jokes())
    receive_task = asyncio.create_task(receive_responses())

    _, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()

    print("[Server] Connection closed")

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=8765, reload=True)
