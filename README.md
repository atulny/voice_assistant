# AI-Voice-Assistant
Welcome to the  Voice Assistant project! This assistant/friend can start conversations, transcribe audio to text, 
generate responses, and convert text back to speech, all while showcasing a sleek frontend interface using Streamlit

## Features
-  Define a assistant/friend
-  Begin a conversation  
-  Transcribe audio to text using an OpenAI model (from Groq).
-  Generate responses quickly with Groq.
-  Convert text back to speech using Google (gTTS).

## Installation

1. If running in Windows, install ffmpeg
   ```bash
    choco install ffmpeg
   ```

2. Clone the repository:
    ```bash
    git clone https://github.com/atulny/voice_assistant.git
   
3. Navigate to the project directory:
    ```bash
    cd  voice-assistant
    ```
4. Create and activate virtual environment:
    ```bash
    python 3.9
    python -m venv venv
    venv/Scripts/activate
    ```
6. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Create a `.env` file using `.env-example` as a template:
    ```bash
    cp .env-example .env
     ```
   and spicify the api keys

2. Run the main application script:
    ```bash
    streamlit run  app.py
    ```
 
