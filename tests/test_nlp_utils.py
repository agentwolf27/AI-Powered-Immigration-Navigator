import unittest
import os
from ..nlp_utils import load_intents, parse_intent, translate_text

# To ensure tests can find 'intents.json', we assume it's in the parent directory
# relative to this test file's location (tests/../intents.json)
INTENTS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'intents.json')

class TestNlpUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load intents data once for all tests in this class."""
        cls.intents_data = load_intents(INTENTS_FILE_PATH)
        if not cls.intents_data or "intents" not in cls.intents_data:
            raise ValueError(f"Could not load or parse intents file at {INTENTS_FILE_PATH} for testing.")

    def test_load_intents(self):
        """Test loading intents from the JSON file."""
        self.assertIsNotNone(self.intents_data)
        self.assertIsInstance(self.intents_data, dict)
        self.assertIn("intents", self.intents_data)
        self.assertIsInstance(self.intents_data["intents"], list)

    def test_parse_intent_known_en_greet(self):
        """Test parsing a known English greeting intent."""
        intent = parse_intent("hello there", "en", self.intents_data)
        self.assertEqual(intent, "greet")

    def test_parse_intent_known_en_visa_status(self):
        """Test parsing a known English visa status intent."""
        intent = parse_intent("check my visa status", "en", self.intents_data)
        self.assertEqual(intent, "check_visa_status")

    def test_parse_intent_known_es_greet(self):
        """Test parsing a known Spanish greeting intent."""
        intent = parse_intent("hola amigo", "es", self.intents_data)
        self.assertEqual(intent, "greet")

    def test_parse_intent_known_es_visa_status(self):
        """Test parsing a known Spanish visa status intent."""
        intent = parse_intent("verificar estado de mi visa", "es", self.intents_data)
        self.assertEqual(intent, "check_visa_status")

    def test_parse_intent_unknown_phrase(self):
        """Test parsing an unknown phrase."""
        intent = parse_intent("this is a completely unknown phrase", "en", self.intents_data)
        self.assertIsNone(intent)

    def test_parse_intent_wrong_language_for_phrase(self):
        """Test parsing a phrase where samples exist but not for the given language."""
        # "hello" is in English samples, but we are asking for Spanish and "hello" isn't in Spanish samples
        intent = parse_intent("hello", "es", self.intents_data)
        # This behavior depends on whether "hello" accidentally matches any Spanish sample.
        # Assuming "hello" is not a substring of any Spanish sample for 'greet' or other intents.
        # Based on current intents.json, "hello" is not in "hola", "buenos días", etc.
        self.assertNotEqual(intent, "greet") # It might match another intent or be None

    def test_parse_intent_no_samples_for_language_key(self):
        """Test parsing when the language key (e.g., samples_fr) doesn't exist in an intent."""
        intent = parse_intent("check my visa status", "fr", self.intents_data) # 'samples_fr' doesn't exist
        self.assertIsNone(intent)

    def test_translate_text_simulated_en_to_es(self):
        """Test the simulated translation for a known phrase."""
        translated = translate_text("hello", "es", "en")
        self.assertEqual(translated, "hola (translated)")

    def test_translate_text_simulated_es_to_en(self):
        """Test the simulated translation for a known phrase from Spanish to English."""
        translated = translate_text("hola", "en", "es")
        self.assertEqual(translated, "hello (translated)")

    def test_translate_text_simulated_unknown_phrase(self):
        """Test the simulated translation for an unknown phrase."""
        original_text = "this is a test"
        target_lang = "de"
        translated = translate_text(original_text, target_lang, "en")
        self.assertEqual(translated, f"{original_text} (simulated translation to {target_lang})")

if __name__ == '__main__':
    unittest.main()
