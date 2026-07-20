from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emotionDetector')
def emotion_detector_function():
    """Emotion detection endpoint - handles blank input with 400 error"""
    text_to_analyze = request.args.get('textToAnalyze', '')
    
    # Check for blank input - return 400 error
    if not text_to_analyze or text_to_analyze.strip() == '':
        return jsonify({
            'error': 'Blank input provided',
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }), 400
    
    # Get emotion analysis
    result = emotion_detector(text_to_analyze)
    
    # Build response string showing all emotions and dominant
    response_string = (
        f"Anger: {result['anger']}, "
        f"Disgust: {result['disgust']}, "
        f"Fear: {result['fear']}, "
        f"Joy: {result['joy']}, "
        f"Sadness: {result['sadness']}, "
        f"Dominant Emotion: {result['dominant_emotion']}"
    )
    
    return response_string

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
