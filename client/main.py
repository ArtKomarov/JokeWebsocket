import asyncio
import websockets
import json
# from translator.gemini_translator import GeminiTranslator
from translator.google_translator import GoogleTranslator

translator = GoogleTranslator()
translation_tasks = set()
MAX_TASKS = 5

async def handle_translation(joke, websocket):
    try:
        translated = await translator.translate_to_german(joke["joke"])
        print(f"[Client] Translated joke {joke['id']}: {translated}")
        response = {
            "id": joke["id"],
            "translated_joke": translated
        }
        await websocket.send(json.dumps(response, ensure_ascii=False))
    except Exception as e:
        print(f"[Client] Error handling joke {joke['id']}: {e}")

async def receive_and_translate():
    uri = "ws://localhost:8765/ws"
    async with websockets.connect(uri) as websocket:
        print("[Client] Connected to server at /ws")
        task_count = 0
        try:
            while True:
                raw = await websocket.recv()
                joke = json.loads(raw)
                print(f"[Client] Received joke {joke['id']}: {joke['joke']}")

                task = asyncio.create_task(handle_translation(joke, websocket))
                translation_tasks.add(task)
                task.add_done_callback(translation_tasks.discard)

                task_count += 1
                if task_count >= MAX_TASKS:
                    print(f"[Client] Reached {MAX_TASKS} tasks, closing connection.")
                    break

        except websockets.exceptions.ConnectionClosed:
            print("[Client] Connection closed")
        
        finally:
            # Wait for all pending translation tasks to complete
            if translation_tasks:
                print("[Client] Waiting for remaining translation tasks to finish...")
                await asyncio.gather(*translation_tasks)

if __name__ == "__main__":
    try:
        asyncio.run(receive_and_translate())
    except KeyboardInterrupt:
        print("\n[Client] Shutting down...")
