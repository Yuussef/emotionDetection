# Emotion Detection Application

## Overview
This project is a web-based emotion detection application that uses IBM Watson NLP to analyze text and identify emotions. The application is built with Flask and provides a simple interface for users to input text and receive emotion analysis results.

## Features
- Detects five emotions: anger, disgust, fear, joy, and sadness
- Identifies the dominant emotion from the analyzed text
- Web interface for easy interaction
- Error handling for blank inputs
- Unit testing with unittest framework
- Static code analysis with pylint

## Project Structure
emotionDetection/
├── EmotionDetection/
│   ├── init.py
│   └── emotion_detection.py
├── server.py
├── test_emotion_detection.py
├── templates/
│   └── index.html
└── README.md
