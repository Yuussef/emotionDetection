from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

API_KEY = "qkU7iUuJTKfK5AB8RVrPNbQZS1e5wDnbqzqGdaBpf7Gf"
URL = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/5f785bf8-f735-4c6a-b54c-d3fa00dfc42e"

authenticator = IAMAuthenticator(apikey=API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
nlu.set_service_url(URL)

def detect_emotion(text):
    try:
        response = nlu.analyze(
            text=text,
            features=Features(emotion=EmotionOptions()),
            language='en'
        )
        emotions = response.result['emotion']['document']['emotion']
        top_emotion = max(emotions, key=emotions.get)
        return top_emotion, round(emotions[top_emotion], 4)
    except Exception as e:
        return "error", 0.0

sentences = [
    "I am so happy!",
    "I hate this",
    "I love you",
    "So sad"
]

for sent in sentences:
    emotion, score = detect_emotion(sent)
    print(f"{sent} -> {emotion} ({score})")

while True:
    text = input("\nEnter text (quit to exit): ")
    if text == 'quit':
        break
    emotion, score = detect_emotion(text)
    print(f"Emotion: {emotion} ({score})")
