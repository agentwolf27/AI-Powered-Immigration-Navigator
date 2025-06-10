from transformers import pipeline

# Simple sentiment analysis placeholder
class MentalHealthBot:
    def __init__(self):
        self.classifier = pipeline('sentiment-analysis')

    def analyze(self, text: str):
        result = self.classifier(text)[0]
        if result['label'] == 'NEGATIVE':
            suggestion = 'Consider speaking with a counselor or practicing relaxation.'
        else:
            suggestion = 'Keep up the positive mindset!'
        return {"sentiment": result['label'], "score": result['score'], "advice": suggestion}
