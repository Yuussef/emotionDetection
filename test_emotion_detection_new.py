import unittest
from EmotionDetection.emotion_detection import emotion_detector

class TestEmotionDetection(unittest.TestCase):
    """Unit tests for emotion detection"""
    
    def test_emotion_detector_returns_dict(self):
        """Test that emotion_detector returns a dictionary"""
        result = emotion_detector("I am happy")
        self.assertIsInstance(result, dict)
    
    def test_happy_text_returns_joy(self):
        """Test that 'I am so happy!' returns dominant emotion of joy"""
        result = emotion_detector("I am so happy!")
        self.assertEqual(result['dominant_emotion'], 'joy')
    
    def test_sad_text_returns_sadness(self):
        """Test that sad text returns dominant emotion of sadness"""
        result = emotion_detector("I am very sad")
        self.assertEqual(result['dominant_emotion'], 'sadness')
    
    def test_angry_text_returns_anger(self):
        """Test that angry text returns dominant emotion of anger"""
        result = emotion_detector("I hate this")
        self.assertEqual(result['dominant_emotion'], 'anger')
    
    def test_dict_has_all_emotions(self):
        """Test that result contains all five emotions"""
        result = emotion_detector("test")
        required_keys = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion']
        for key in required_keys:
            self.assertIn(key, result)
    
    def test_emotion_scores_numeric(self):
        """Test that emotion scores are numeric values"""
        result = emotion_detector("I am happy")
        for emotion in ['anger', 'disgust', 'fear', 'joy', 'sadness']:
            self.assertTrue(isinstance(result[emotion], (int, float)) or result[emotion] is None)
    
    def test_empty_string_returns_result(self):
        """Test handling of empty string"""
        result = emotion_detector("")
        self.assertIsNotNone(result)
        self.assertIn('dominant_emotion', result)
    
    def test_long_text_returns_joy(self):
        """Test with longer text"""
        text = "I am absolutely thrilled and delighted with this wonderful news!"
        result = emotion_detector(text)
        self.assertEqual(result['dominant_emotion'], 'joy')
    
    def test_error_handling(self):
        """Test error handling returns valid structure"""
        result = emotion_detector("test")
        self.assertIsNotNone(result)
        self.assertIn('dominant_emotion', result)

if __name__ == '__main__':
    unittest.main()
