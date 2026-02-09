#!/usr/bin/env python
"""
Test script to verify the Voice Emotion Analysis application
"""

import sys
import os

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✓ Flask")
        
        import numpy
        print("✓ NumPy")
        
        import librosa
        print("✓ librosa")
        
        import soundfile
        print("✓ soundfile")
        
        import torch
        print("✓ PyTorch")
        
        import transformers
        print("✓ Transformers")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_modules():
    """Test that custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from audio_processing.preprocess import AudioProcessor
        print("✓ AudioProcessor")
        
        from emotion_model.model import EmotionDetector
        print("✓ EmotionDetector")
        
        return True
    except ImportError as e:
        print(f"✗ Module import failed: {e}")
        return False

def test_initialization():
    """Test that components can be initialized"""
    print("\nTesting initialization...")
    
    try:
        from audio_processing.preprocess import AudioProcessor
        from emotion_model.model import EmotionDetector
        
        processor = AudioProcessor()
        print("✓ AudioProcessor initialized")
        
        detector = EmotionDetector()
        print("✓ EmotionDetector initialized")
        
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False

def test_directory_structure():
    """Test that required directories exist"""
    print("\nTesting directory structure...")
    
    dirs = [
        'uploads',
        'templates',
        'static/css',
        'static/js',
        'emotion_model',
        'audio_processing'
    ]
    
    all_exist = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 60)
    print("Voice Emotion Analysis - System Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Modules", test_modules()))
    results.append(("Initialization", test_initialization()))
    results.append(("Directory Structure", test_directory_structure()))
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! Application is ready to run.")
        print("\nTo start the application, run:")
        print("  python app.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Check directory structure")
        print("  - Verify Python version >= 3.11")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
