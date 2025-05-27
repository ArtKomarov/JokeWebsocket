import os
import json
import asyncio
import uvicorn
import re
import logging
import structlog
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from google import genai
from google.genai import types

load_dotenv()

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configure logging
logging.basicConfig(format="%(message)s", level=logging.INFO)

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
)

logger = structlog.get_logger()


async def generate_jokes_batch(n: int) -> list[dict]:
    prompt = (
        f"Generate {n} short, funny English jokes. "
        "Return them as a JSON array of objects in the format: "
        '[{"id":1,"joke":"...joke1..."}, {"id":2,"joke":"...joke2..."}, ...]. '
    )
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a JSON generator. Respond ONLY with the JSON, no extra text.",
            ),
            contents=prompt
        )
        jokes_json_str = response.text.strip()
        jokes_json_str = strip_code_fences_if_present(jokes_json_str)

        logger.info("Received jokes JSON", jokes_json_preview=jokes_json_str[:300] + "...")

        jokes = json.loads(jokes_json_str)
        return jokes
    except Exception as e:
        logger.error("Joke batch generation error", exception=str(e))
        # TODO: Replace with a proper fallback mechanism: e.g. use old version and load from file.
        return [{"id": i + 1, "joke": "Fallback joke"} for i in range(n)]

def strip_code_fences_if_present(text: str) -> str:
    text = text.strip()
    if text.startswith("```json") or text.startswith("```"):
        return re.sub(r"^```json?\n|```$", "", text, flags=re.MULTILINE)

    return text

@app.on_event("startup")
async def startup_event():
    # Generate 20 jokes at startup and store in app state
    logger.info("Generating jokes...")
    app.state.jokes = await generate_jokes_batch(20)
    logger.info("Jokes generated.")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected to /ws")
    jokes = app.state.jokes

    async def send_jokes():
        try:
            while True:
                for joke in jokes:
                    await websocket.send_json(joke)
                    await asyncio.sleep(0.2)
        except Exception as e:
            logger.error("send_jokes error", exception=str(e))

    async def receive_responses():
        while True:
            try:
                response = await websocket.receive_text()
                logger.info("Received from client", response=response)
            except WebSocketDisconnect:
                logger.warning("Client disconnected")
                break
            except Exception as e:
                logger.error("Error receiving response", exception=str(e))
                break


    send_task = asyncio.create_task(send_jokes())
    receive_task = asyncio.create_task(receive_responses())

    _, pending = await asyncio.wait(
        [send_task, receive_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()

    logger.info("Connection closed")

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=8765, reload=True)
