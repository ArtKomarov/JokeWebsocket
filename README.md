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

- Python 3.9+
- FastAPI
- Uvicorn
- websockets
- google-cloud-translate (if using Google Translate)
- google-genai (if using Gemini)
- python-dotenv (for managing API keys)
  
---

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/joke-websocket.git
    cd joke-websocket
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

4. Prepare your API keys:

    - For Google Translate, set up Google Cloud Translate credentials and export `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to your JSON key file.
    - For Gemini API, create a `.env` file and add your key as `GEMINI_API_KEY=your_api_key_here`

    Example `.env`:

    ```bash
    GEMINI_API_KEY=your_api_key_here
    GOOGLE_APPLICATION_CREDENTIALS=your_key_file_path_here
    ```

5. Run the server:

    ```bash
    uvicorn server.main:app --host 127.0.0.1 --port 8765 --reload
    ```

6. Run the client:

    ```bash
    python client/main.py
    ```