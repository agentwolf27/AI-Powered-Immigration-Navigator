import unittest
from ..mental_bot import (
    get_greeting,
    get_wellness_check_question,
    get_empathetic_response,
    chat_round,
    GREETINGS,
    WELLNESS_CHECKS,
    EMPATHETIC_RESPONSES,
    DEFAULT_RESPONSES
)

class TestMentalBot(unittest.TestCase):

    def test_get_greeting(self):
        """Test if get_greeting returns a non-empty string from defined greetings."""
        greeting = get_greeting()
        self.assertIsInstance(greeting, str)
        self.assertTrue(len(greeting) > 0)
        self.assertIn(greeting, GREETINGS)

    def test_get_wellness_check_question(self):
        """Test if get_wellness_check_question returns a non-empty string from defined questions."""
        question = get_wellness_check_question()
        self.assertIsInstance(question, str)
        self.assertTrue(len(question) > 0)
        self.assertIn(question, WELLNESS_CHECKS)

    def test_get_empathetic_response_known_keyword(self):
        """Test empathetic response for a known keyword."""
        user_input = "I'm feeling sad today."
        response = get_empathetic_response(user_input)
        self.assertEqual(response, EMPATHETIC_RESPONSES["sad"])

    def test_get_empathetic_response_another_known_keyword(self):
        """Test empathetic response for another known keyword."""
        user_input = "I am so stressed with work."
        response = get_empathetic_response(user_input)
        self.assertEqual(response, EMPATHETIC_RESPONSES["stressed"])

    def test_get_empathetic_response_unknown_keyword(self):
        """Test empathetic response for an unknown keyword (should return a default response)."""
        user_input = "The weather is nice."
        response = get_empathetic_response(user_input)
        self.assertIn(response, DEFAULT_RESPONSES)

    def test_chat_round_initial(self):
        """Test chat_round with no input (initial interaction)."""
        response = chat_round(user_input=None)
        self.assertIsInstance(response, str)
        self.assertTrue(any(g in response for g in GREETINGS))
        self.assertTrue(any(w in response for w in WELLNESS_CHECKS))

    def test_chat_round_follow_up(self):
        """Test chat_round with some user input."""
        user_input = "I'm feeling a bit anxious."
        response = chat_round(user_input=user_input)
        self.assertIsInstance(response, str)
        # Check if it contains the empathetic response for "anxious"
        # and potentially another wellness check.
        self.assertIn(EMPATHETIC_RESPONSES["anxious"], response)

if __name__ == '__main__':
    unittest.main()
