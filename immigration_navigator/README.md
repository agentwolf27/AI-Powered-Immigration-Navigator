# AI Immigration Navigator

This folder contains the backend and simple frontend for the AI Immigration Navigator demo.

## Setup

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server
   ```bash
   uvicorn immigration_navigator.backend.app:app --reload
   ```

3. Open `http://localhost:8000/` in your browser.

The backend exposes several endpoints under `/api/` for immigration guidance, form generation, wellness checks, translation, and timelines.
