from flask import Flask, request, jsonify

# Import functions from our modules
from law_flow import (
    get_visa_types,
    get_visa_stages,
    get_required_documents,
    get_immigration_steps,
    get_document_details
)
from mental_bot import (
    chat_round as mental_chat_round, # Renamed to avoid conflict if we had a generic chat_round
    load_mental_bert_model,
    get_greeting as get_mental_greeting,
    get_empathetic_response as get_mental_empathetic_response
)
from nlp_utils import (
    load_intents,
    parse_intent,
    translate_text
)

# Initialize Flask App
app = Flask(__name__)

# Load initial data
intents_data = load_intents() # Load from intents.json
if not intents_data:
    print("Warning: Intents data could not be loaded. Intent parsing will not work.")
    # Provide a default structure to prevent errors if intents_data is None
    intents_data = {"intents": []}


# Simulate loading the mental health model (as per mental_bot.py)
load_mental_bert_model()

# --- Helper function for error handling ---
def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

# --- API Endpoints ---

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    """
    General query handling endpoint.
    Accepts: {"text": "user input", "language": "en"}
    Returns: {"response": "bot's answer", "intent": "detected_intent"}
    """
    data = request.get_json()
    if not data:
        return bad_request("No JSON data provided.")

    user_text = data.get('text')
    language = data.get('language', 'en') # Default to English if not provided

    if not user_text:
        return bad_request("Missing 'text' field in JSON data.")

    # 1. Parse Intent
    detected_intent = parse_intent(user_text, language, intents_data)
    bot_response = "Could not understand the request." # Default response

    # 2. Formulate response based on intent
    if detected_intent == "greet":
        response_text = get_mental_greeting() # Using mental bot's greeting for now
        if language != 'en':
            # Simulate translation if a different language is requested
            # For a real app, the greeting itself might need to be language-specific before this step
            response_text = translate_text(response_text, language, "en")
        bot_response = response_text
    elif detected_intent == "ask_mental_wellness" or detected_intent == "get_help_mental":
        # Delegate to mental_bot
        # We might need to translate user_text to English if mental_bot only understands English
        text_for_mental_bot = user_text
        if language != 'en':
            text_for_mental_bot = translate_text(user_text, "en", language) # Translate to EN for the bot

        mental_response = mental_chat_round(user_input=text_for_mental_bot)

        # Translate mental_response back to user's language if needed
        if language != 'en':
            mental_response = translate_text(mental_response, language, "en")
        bot_response = mental_response

    elif detected_intent in ["check_visa_status", "ask_visa_types"]:
        # Placeholder for law-related intents
        # For a real scenario, you might extract entities (country, visa type) here
        # and call specific law_flow functions.
        response_text = f"This query (intent: {detected_intent}) would be handled by the immigration module. For example, try the /immigration endpoint for specific details."
        if language != 'en':
            response_text = translate_text(response_text, language, "en")
        bot_response = response_text
        # Example: If intent is ask_visa_types, you might try to extract a country
        # if "US" in user_text or "America" in user_text:
        #     visas = get_visa_types("US")
        #     bot_response = f"Available visa types for US: {', '.join(visas)}"
        # elif "Canada" in user_text:
        #     visas = get_visa_types("CA")
        #     bot_response = f"Available visa types for Canada: {', '.join(visas)}"

    elif detected_intent == "farewell":
        response_text = "Goodbye! Take care."
        if language != 'en':
            response_text = translate_text(response_text, language, "en")
        bot_response = response_text
    else: # No intent or unknown
        response_text = "I'm not sure how to help with that. Can you try rephrasing?"
        if language != 'en':
            response_text = translate_text(response_text, language, "en")
        bot_response = response_text

    return jsonify({"response": bot_response, "intent": detected_intent or "unknown"})

@app.route('/immigration', methods=['POST'])
def immigration_endpoint():
    """
    Handles immigration-specific queries.
    Accepts: {"country": "US", "visa_type": "H-1B", "stage": "Petition Filing", "language": "en"}
    Returns: {"steps": ["step1", "step2"], "documents": ["doc1", "doc2"]}
    """
    data = request.get_json()
    if not data:
        return bad_request("No JSON data provided.")

    country = data.get('country')
    visa_type = data.get('visa_type')
    stage = data.get('stage')
    language = data.get('language', 'en') # Default to English

    if not all([country, visa_type, stage]):
        return bad_request("Missing one or more fields: 'country', 'visa_type', 'stage'.")

    # Get information from law_flow
    steps = get_immigration_steps(country, visa_type, stage)
    documents = get_required_documents(visa_type, stage)

    # Simulate translation if language is not English
    # In a real app, the content from law_flow itself might need to be available in multiple languages
    if language != 'en':
        steps = [translate_text(step, language, "en") for step in steps]
        documents = [translate_text(doc, language, "en") for doc in documents]

    return jsonify({
        "country": country,
        "visa_type": visa_type,
        "current_stage": stage,
        "next_steps": steps,
        "required_documents_for_current_stage": documents
    })

@app.route('/wellness', methods=['POST'])
def wellness_endpoint():
    """
    Handles mental wellness check-ins.
    Accepts: {"text": "user feeling", "language": "en"} (or GET for initial greeting)
    Returns: {"response": "bot's empathetic reply"}
    """
    data = request.get_json()
    if not data:
        return bad_request("No JSON data provided.") # Assuming POST for conversation

    user_text = data.get('text')
    language = data.get('language', 'en')

    if user_text is None: # text can be an empty string if user just wants initial message
        return bad_request("Missing 'text' field in JSON data for POST request.")

    # Text for the bot (potentially translate to English if bot is EN only)
    text_for_bot = user_text
    if language != 'en':
        text_for_bot = translate_text(user_text, "en", language)

    bot_reply = mental_chat_round(user_input=text_for_bot)

    # Translate bot's reply back to user's language if needed
    if language != 'en':
        bot_reply = translate_text(bot_reply, language, "en")

    return jsonify({"response": bot_reply})

@app.route('/wellness/greeting', methods=['GET'])
def wellness_greeting_endpoint():
    """
    Provides an initial greeting and wellness check question from the mental bot.
    Accepts query param: ?language=es (optional)
    Returns: {"response": "bot's greeting and question"}
    """
    language = request.args.get('language', 'en')

    # Get initial message (greeting + wellness question)
    greeting_and_question = mental_chat_round(user_input=None) # Gets the initial message

    if language != 'en':
        greeting_and_question = translate_text(greeting_and_question, language, 'en')

    return jsonify({"response": greeting_and_question})


if __name__ == '__main__':
    # Note: In a production environment, use a proper WSGI server like Gunicorn or Waitress.
    # app.run(debug=True) is suitable for development.
    app.run(debug=True, host='0.0.0.0', port=5000)
