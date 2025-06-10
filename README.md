# AI Immigration + Wellness Assistant Prototype

This project is a prototype for an AI assistant that helps users with immigration processes and provides mental wellness checks. It features modular components for legal information, chatbot interactions, and multi-language support.

## Project Structure

- `app.py`: Main Flask application with API endpoints.
- `law_flow.py`: Handles immigration-related logic, visa information, and procedural steps (currently uses placeholder data).
- `mental_bot.py`: Powers the mental wellness chatbot, providing empathetic responses (simulated model and placeholder conversation data).
- `nlp_utils.py`: Contains utilities for Natural Language Processing, including intent parsing and simulated translation.
- `tts_asr.py`: Provides placeholder functions and comments outlining potential integration of Text-to-Speech (TTS) and Speech-to-Text (ASR) pipelines using resources like CommonVoice and Tatoeba.
- `intents.json`: Stores sample intents for multi-language intent parsing (English and Spanish examples included).
- `data/`: Directory intended for storing datasets (currently empty).
- `models/`: Directory intended for storing pre-trained models (currently empty).
- `tests/`: Contains unit tests for the application modules.

## Setup and Running

1.  **Prerequisites:**
    - Python 3.x
    - Flask (`pip install Flask`)

2.  **Running the Application:**
    ```bash
    python app.py
    ```
    The application will start on `http://127.0.0.1:5000`. (Note: The current `app.py` runs on `0.0.0.0:5000`)

3.  **Running Tests:**
    Navigate to the project's root directory and run:
    ```bash
    python -m unittest discover -s tests
    ```

## API Endpoints

### 1. Chat (`/chat`)
- **Method:** `POST`
- **Description:** General-purpose endpoint for interacting with the assistant. It parses intent and routes to appropriate modules.
- **Request Body (JSON):**
  ```json
  {
    "text": "user's message",
    "language": "en" // or "es", etc.
  }
  ```
- **Example Response (JSON):**
  ```json
  {
    "response": "Hello! How can I help you today?",
    "intent": "greet"
  }
  ```

### 2. Immigration Info (`/immigration`)
- **Method:** `POST`
- **Description:** Provides immigration steps and required documents based on user's situation.
- **Request Body (JSON):**
  ```json
  {
    "country": "US",
    "visa_type": "H-1B",
    "stage": "Petition Filing",
    "language": "en"
  }
  ```
- **Example Response (JSON):**
  ```json
  {
    "next_steps": ["Submit Form I-129", "Await USCIS decision"],
    "required_documents_for_current_stage": ["Completed Form I-129", "Copy of Passport", "Educational Transcripts"]
  }
  ```

### 3. Wellness Check - Greeting (`/wellness/greeting`)
- **Method:** `GET`
- **Description:** Gets an initial greeting and wellness check question from the mental health bot.
- **Example Response (JSON):**
  ```json
  {
    "response": "Hello, I'm here to listen. How are you feeling today?"
  }
  ```

### 4. Wellness Check - Chat (`/wellness`)
- **Method:** `POST`
- **Description:** Sends user input to the mental wellness bot for an empathetic response.
- **Request Body (JSON):**
  ```json
  {
    "text": "I'm feeling a bit stressed.",
    "language": "en"
  }
  ```
- **Example Response (JSON):**
  ```json
  {
    "response": "It sounds like you're going through a lot. Take a deep breath."
  }
  ```

## Further Development Ideas
- Integrate actual legal datasets (Data.gov, Migration Data Portal).
- Load and use real pre-trained models (MentalBERT, XLM-RoBERTa).
- Implement full TTS/ASR capabilities using CommonVoice/Tatoeba.
- Expand `intents.json` based on MASSIVE dataset structure.
- Develop more sophisticated NLP logic for intent parsing and entity extraction.
- Connect to BabelNet for vocabulary normalization.