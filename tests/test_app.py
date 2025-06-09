import unittest
import json
from ..app import app # Relative import from parent directory

class TestAppEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up a test client for the Flask application."""
        self.app = app
        self.client = self.app.test_client()
        # Ensure intents are loaded for tests that rely on them
        # This assumes app.py already loads intents_data globally
        # If app.intents_data is not loaded, tests might fail or need mocking
        if not self.app.intents_data or not self.app.intents_data.get("intents"):
            print("Warning: app.intents_data not loaded or empty in test_app.py setUp. Forcing load.")
            # This is a bit of a hack for testing; ideally, app initialization handles this robustly.
            # Or, we could mock nlp_utils.load_intents within the app for tests.
            from ..nlp_utils import load_intents as util_load_intents
            import os
            INTENTS_FILE_PATH_FOR_TEST = os.path.join(os.path.dirname(__file__), '..', 'intents.json')
            self.app.intents_data = util_load_intents(INTENTS_FILE_PATH_FOR_TEST)


    def test_chat_greet_en(self):
        """Test the /chat endpoint with an English greeting."""
        payload = {"text": "hello", "language": "en"}
        response = self.client.post('/chat', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertEqual(data.get("intent"), "greet")

    def test_chat_greet_es(self):
        """Test the /chat endpoint with a Spanish greeting."""
        payload = {"text": "hola", "language": "es"}
        response = self.client.post('/chat', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertEqual(data.get("intent"), "greet")
        self.assertIn("hola", data["response"].lower()) # Check if "hola" is in the (translated) response

    def test_chat_mental_wellness_en(self):
        """Test /chat with a mental wellness query in English."""
        payload = {"text": "I am feeling sad", "language": "en"}
        response = self.client.post('/chat', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertIn(data.get("intent"), ["ask_mental_wellness", "get_help_mental"]) # "sad" is in EMPATHETIC_RESPONSES
        self.assertTrue("sad" in data["response"] or "sorry to hear" in data["response"])


    def test_immigration_endpoint_valid(self):
        """Test the /immigration endpoint with valid data."""
        payload = {"country": "US", "visa_type": "H-1B", "stage": "Petition Filing", "language": "en"}
        response = self.client.post('/immigration', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("next_steps", data)
        self.assertIsInstance(data["next_steps"], list)
        self.assertIn("required_documents_for_current_stage", data)
        self.assertIsInstance(data["required_documents_for_current_stage"], list)

    def test_immigration_endpoint_missing_fields(self):
        """Test the /immigration endpoint with missing fields."""
        payload = {"country": "US", "visa_type": "H-1B"} # Missing "stage"
        response = self.client.post('/immigration', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertTrue("Missing one or more fields" in data["error"])

    def test_wellness_greeting_endpoint(self):
        """Test the GET /wellness/greeting endpoint."""
        response = self.client.get('/wellness/greeting?language=en')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertTrue(len(data["response"]) > 0)

    def test_wellness_chat_endpoint_en(self):
        """Test the POST /wellness endpoint in English."""
        payload = {"text": "I'm feeling a bit down today.", "language": "en"}
        response = self.client.post('/wellness', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertTrue(len(data["response"]) > 0)

    def test_chat_missing_text_field(self):
        """Test /chat endpoint with missing 'text' field."""
        payload = {"language": "en"} # Missing "text"
        response = self.client.post('/chat', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing 'text' field in JSON data.")

    def test_chat_no_json_data(self):
        """Test /chat endpoint with no JSON data."""
        response = self.client.post('/chat', data="this is not json", content_type="text/plain")
        self.assertEqual(response.status_code, 400) # Flask 1.0+ typically returns 400 for non-JSON if request.get_json() is used
        data = json.loads(response.data)
        self.assertIn("error", data)
        # The exact error message can vary based on Flask version and how it handles malformed JSON
        self.assertTrue("No JSON data provided." in data["error"] or "Failed to decode JSON object" in data["error"] or "Not a JSON" in data["error"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
