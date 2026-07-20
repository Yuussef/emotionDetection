"""
Packaging Test - Validates emotion_detection is a valid package
"""

import sys
import importlib.util
import os

def test_module_exists():
    """Test if emotion_detection.py exists"""
    assert os.path.isfile('emotion_detection.py'), "emotion_detection.py not found"
    print("✓ emotion_detection.py exists")

def test_module_imports():
    """Test if emotion_detection module can be imported"""
    spec = importlib.util.spec_from_file_location("emotion_detection", "emotion_detection.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("✓ emotion_detection module imports successfully")

def test_has_required_functions():
    """Test if emotion_detection has required functions"""
    spec = importlib.util.spec_from_file_location("emotion_detection", "emotion_detection.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    assert hasattr(module, 'detect_emotion'), "detect_emotion function not found"
    print("✓ detect_emotion function exists")

def test_function_returns_tuple():
    """Test if detect_emotion returns (emotion, score)"""
    spec = importlib.util.spec_from_file_location("emotion_detection", "emotion_detection.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    emotion, score = module.detect_emotion("I am happy")
    assert isinstance(emotion, str), "Emotion should be string"
    assert isinstance(score, (int, float)), "Score should be numeric"
    print(f"✓ detect_emotion returns valid tuple: ({emotion}, {score})")

def test_watson_credentials():
    """Test if Watson credentials are set"""
    spec = importlib.util.spec_from_file_location("emotion_detection", "emotion_detection.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    assert hasattr(module, 'API_KEY'), "API_KEY not found"
    assert hasattr(module, 'URL'), "URL not found"
    assert module.API_KEY != "", "API_KEY is empty"
    assert module.URL != "", "URL is empty"
    print("✓ Watson NLP credentials configured")

def test_watson_nlu_initialized():
    """Test if NLU service is initialized"""
    spec = importlib.util.spec_from_file_location("emotion_detection", "emotion_detection.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    assert hasattr(module, 'nlu'), "NLU service not initialized"
    print("✓ Watson NLU service initialized")

def run_all_tests():
    """Run all packaging tests"""
    print("\n" + "="*60)
    print("PACKAGING TEST - emotion_detection Validation")
    print("="*60 + "\n")
    
    tests = [
        test_module_exists,
        test_module_imports,
        test_has_required_functions,
        test_watson_credentials,
        test_watson_nlu_initialized,
        test_function_returns_tuple,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    if failed == 0:
        print("✅ emotion_detection is a VALID PACKAGE!")
    else:
        print("❌ Some tests failed")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
