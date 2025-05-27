# Joke WebSocket Translator

A simple WebSocket-based joke server and client with live translation.

## Overview

This project consists of two components communicating over WebSockets:

- **Joke Server**:  
  A FastAPI WebSocket server that streams jokes every 200ms from a static list.

- **Joke Client**:  
  Connects to the server, receives jokes, translates them to German using an external API (e.g., Google Translate or Gemini),  
  and sends back the translated joke as JSON. Handles multiple concurrent translations and closes after sending 5 translated jokes.

---

## Features

- WebSocket communication with asynchronous concurrency
- Sends jokes in JSON format `{ "id": int, "joke": str }`
- Client translates jokes to German using an external translation API
- Client sends back JSON responses `{ "id": int, "translated_joke": str }`
- Connection remains open during joke streaming and translation
- Limits client to 5 translated jokes before disconnecting

---

## Requirements

Check `requirements.txt`.
  
---

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/ArtKomarov/JokeWebsocket.git
    cd JokeWebsocket
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Prepare your API keys (see below).

5. Run the server:

    ```bash
    python -m uvicorn server.main:app --host 127.0.0.1 --port 8765 --reload
    ```

6. Run the client:

    ```bash
    python client/main.py
    ```


---

## How to Get API Keys

### Google Translate (`GOOGLE_APPLICATION_CREDENTIALS`)

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).

2. Enable **Cloud Translation API** for your project.

3. Create a **Service Account** under **APIs & Services > Credentials**.

4. Generate and download a **JSON key** for the service account.

5. Set environment variable `GOOGLE_APPLICATION_CREDENTIALS` pointing to the JSON key file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"
   ```
   Or add this line to your .env file.

More info: [setup docs](https://cloud.google.com/translate/docs/setup)

### Gemini API (`GEMINI_API_KEY`)

1. [Get Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) (may require requesting access).

2. Set environment variable `GEMINI_API_KEY`:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
   Or add this line to your .env file.
