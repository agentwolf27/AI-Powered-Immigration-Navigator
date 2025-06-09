import json

def load_intents(filepath: str = "intents.json") -> dict:
    """
    Loads the intents from the specified JSON file.

    Args:
        filepath (str): The path to the intents JSON file.

    Returns:
        dict: The loaded intents data, or an empty dictionary if loading fails.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            intents_data = json.load(f)
        return intents_data
    except FileNotFoundError:
        print(f"Error: Intents file not found at {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return {}

def parse_intent(text: str, language: str, intents_data: dict) -> str | None:
    """
    Parses the user text to identify an intent based on sample phrases.
    This is a basic implementation using simple substring matching.

    Args:
        text (str): The user's input text.
        language (str): The language code (e.g., "en", "es").
        intents_data (dict): The loaded intents data.

    Returns:
        str | None: The name of the matched intent, or None if no intent is matched.
    """
    if not intents_data or "intents" not in intents_data:
        return None

    text_lower = text.lower()
    sample_key = f"samples_{language}" # e.g., "samples_en" or "samples_es"

    for intent_info in intents_data["intents"]:
        if sample_key in intent_info:
            for sample_phrase in intent_info[sample_key]:
                if sample_phrase.lower() in text_lower:
                    return intent_info["name"]
    return None

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Simulates text translation.
    For demonstration, it returns the original text with a note,
    or a hardcoded translation for a specific example.

    Args:
        text (str): The text to translate.
        target_language (str): The target language code (e.g., "es").
        source_language (str): The source language code (e.g., "en").

    Returns:
        str: The translated text (simulated).
    """
    print(f"Simulating translation of '{text}' from {source_language} to {target_language}.")
    if text.lower() == "hello" and target_language == "es":
        return "hola (translated)"
    if text.lower() == "hola" and target_language == "en":
        return "hello (translated)"
    # Add more hardcoded examples if needed for specific demonstrations
    return f"{text} (simulated translation to {target_language})"

if __name__ == '__main__':
    # Example Usage
    intents = load_intents() # Assumes intents.json is in the same directory

    if intents:
        print("--- Intent Parsing ---")
        # English examples
        print(f"'hello there' -> Intent: {parse_intent('hello there', 'en', intents)}")
        print(f"'Can you check my visa status?' -> Intent: {parse_intent('Can you check my visa status?', 'en', intents)}")
        print(f"'I need help' -> Intent: {parse_intent('I need help', 'en', intents)}")
        print(f"'What types of visas for US?' -> Intent: {parse_intent('What types of visas for US?', 'en', intents)}")

        # Spanish examples
        print(f"'hola amigo' -> Intent: {parse_intent('hola amigo', 'es', intents)}")
        print(f"'verificar estado de mi visa por favor' -> Intent: {parse_intent('verificar estado de mi visa por favor', 'es', intents)}")
        print(f"'Necesito ayuda con mi ansiedad' -> Intent: {parse_intent('Necesito ayuda con mi ansiedad', 'es', intents)}")

        # No match
        print(f"'this should not match' -> Intent: {parse_intent('this should not match', 'en', intents)}")
        print(f"'greetings Earthling' -> Intent (es): {parse_intent('greetings Earthling', 'es', intents)}") # No es samples for greet with this
        print(f"'check my visa status' (with 'fr' key missing) -> Intent: {parse_intent('check my visa status', 'fr', intents)}")


    print("\n--- Text Translation (Simulation) ---")
    print(f"Translate 'hello' to Spanish: {translate_text('hello', 'es')}")
    print(f"Translate 'hola' to English: {translate_text('hola', 'en', source_language='es')}")
    print(f"Translate 'good morning' to French: {translate_text('good morning', 'fr')}")
    print(f"Translate 'buenas tardes' to English: {translate_text('buenas tardes', 'en', source_language='es')}")

    # Test loading a non-existent file
    print("\n--- Testing Non-existent Intents File ---")
    non_existent_intents = load_intents("non_existent_intents.json")
    print(f"Result of loading non_existent_intents.json: {non_existent_intents}")
    print(f"'hello there' with no intents data -> Intent: {parse_intent('hello there', 'en', non_existent_intents)}")
