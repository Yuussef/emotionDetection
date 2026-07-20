import requests
import json

def emotion_detector(text_to_analyse):
    """
    Detect emotions using Watson NLP API
    
    Args:
        text_to_analyse: Text string to analyze for emotions
        
    Returns:
        Dictionary with emotion scores and dominant emotion
    """
    
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    payload = {
        "raw_document": {
            "text": text_to_analyse
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # Handle 400 errors - bad request
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        # Parse response
        response_json = response.json()
        emotions = response_json['emotionPredictor']['emotion']
        
        # Find dominant emotion (highest score)
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Return all emotions with dominant emotion
        return {
            'anger': round(emotions.get('anger', 0), 4),
            'disgust': round(emotions.get('disgust', 0), 4),
            'fear': round(emotions.get('fear', 0), 4),
            'joy': round(emotions.get('joy', 0), 4),
            'sadness': round(emotions.get('sadness', 0), 4),
            'dominant_emotion': dominant_emotion
        }
        
    except requests.exceptions.RequestException as e:
        # Return None values on error
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }


if __name__ == "__main__":
    # Test sentences
    sentences = [
        "I am so happy!",
        "I hate this",
        "I love you",
        "So sad"
    ]
    
    for sent in sentences:
        result = emotion_detector(sent)
        print(result)
    
    # Interactive loop
    while True:
        text = input("\nEnter text (quit to exit): ")
        if text == 'quit':
            break
        result = emotion_detector(text)
        print(result)
