import random

# 1. Simulate Model Loading
def load_mental_bert_model():
    """Simulates loading a MentalBERT model."""
    print("MentalBERT model loaded (simulated).")

# Call the function at the beginning of the script
load_mental_bert_model()

# 2. Define Placeholder Conversation Data

# GREETINGS: A list of initial greetings the bot can use
GREETINGS = [
    "Hello there! I'm here to listen. How are you doing today?",
    "Hi! It's good to connect. What's on your mind?",
    "Hey! I hope you're having an okay day. Want to talk about anything?",
    "Greetings! I'm your friendly support bot. How can I help you feel a bit better today?"
]

# WELLNESS_CHECKS: A list of questions the bot can ask to check on the user's mental state
WELLNESS_CHECKS = [
    "How are you feeling today, really?",
    "Is there anything on your mind that you'd like to share?",
    "What kind of thoughts have you been having lately?",
    "On a scale of 1 to 10, how would you rate your current mood?",
    "Remember, I'm here to listen without judgment. What's up?"
]

# EMPATHETIC_RESPONSES: A dictionary mapping keywords or sentiment (simulated) to empathetic responses
EMPATHETIC_RESPONSES = {
    "sad": "I'm sorry to hear you're feeling sad. Remember it's okay to feel this way, and you're not alone.",
    "stressed": "It sounds like you're going through a lot. Take a deep breath; we can explore ways to manage this stress if you like.",
    "anxious": "Anxiety can be really tough. I'm here for you. Sometimes just talking about it can help.",
    "lonely": "Feeling lonely is a difficult emotion. Thank you for sharing that with me. I'm here to keep you company.",
    "happy": "That's wonderful to hear you're feeling happy! What's bringing you joy?",
    "angry": "It's understandable to feel angry sometimes. What's causing this feeling for you?",
    "tired": "Feeling tired can make everything seem harder. Make sure you're giving yourself time to rest."
}

# DEFAULT_RESPONSES: A list of responses to use when the bot doesn't have a specific empathetic response
DEFAULT_RESPONSES = [
    "Thank you for sharing that with me. It takes courage to open up.",
    "I'm here to listen. Tell me more if you feel comfortable.",
    "That sounds important. How is it affecting you?",
    "I understand. Sometimes just expressing our feelings can make a difference.",
    "Remember to be kind to yourself."
]

# 3. Create Core Chatbot Functions

def get_greeting() -> str:
    """Returns a random greeting."""
    return random.choice(GREETINGS)

def get_wellness_check_question() -> str:
    """Returns a random wellness check question."""
    return random.choice(WELLNESS_CHECKS)

def get_empathetic_response(user_input: str) -> str:
    """
    Takes user input (simulated analysis), and returns an appropriate
    empathetic response based on keywords or a default response.
    This function simulates understanding user input for now.
    """
    user_input_lower = user_input.lower()
    for keyword, response in EMPATHETIC_RESPONSES.items():
        if keyword in user_input_lower:
            return response
    return random.choice(DEFAULT_RESPONSES)

# 4. Basic Conversation Flow Logic

def chat_round(user_input: str = None) -> str:
    """
    Manages a round of conversation.
    - If user_input is None (first interaction), returns a greeting and a wellness check question.
    - If user_input is provided, it calls get_empathetic_response and then perhaps asks another wellness question.
    """
    if user_input is None:
        return f"{get_greeting()} {get_wellness_check_question()}"
    else:
        empathetic_response = get_empathetic_response(user_input)
        # For now, let's follow up with another wellness check or a kind remark
        if random.random() < 0.7: # 70% chance to ask another question
            return f"{empathetic_response} {get_wellness_check_question()}"
        else:
            return f"{empathetic_response} Remember, I'm here if you want to talk more."

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    print("Bot's first message:")
    print(chat_round())
    print("\nUser says: I'm feeling a bit sad today.")
    print("Bot's response:")
    print(chat_round("I'm feeling a bit sad today."))
    print("\nUser says: I am so stressed with work.")
    print("Bot's response:")
    print(chat_round("I am so stressed with work."))
    print("\nUser says: I don't know, just thinking.")
    print("Bot's response:")
    print(chat_round("I don't know, just thinking."))
    print("\nUser says: I'm actually happy today!")
    print("Bot's response:")
    print(chat_round("I'm actually happy today!"))

    # Test individual functions
    print("\n--- Testing individual functions ---")
    print("Random greeting:", get_greeting())
    print("Random wellness check:", get_wellness_check_question())
    print("Empathetic response for 'lonely':", get_empathetic_response("I feel lonely"))
    print("Default empathetic response:", get_empathetic_response("The sky is blue."))
