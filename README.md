# -AI-Powered-Tool-for-Combating-Misinformation
This AI-powered browser extension helps users detect and verify misinformation online. It uses AI algorithms to fact-check text, images, and sources, cross-references content with trusted websites, and incorporates community feedback to flag suspicious information.


Features
Detect fake news in real-time via Chrome extension or web form.
Deep Learning (LSTM) model for text classification.
OCR support to analyze news from images.
URL extraction for scraping news articles.
Easy integration via a local Flask server.


How It Works

Chrome Extension:

User pastes or selects a news snippet.
Sends text to local Flask API (/predict_json).
Displays prediction and confidence.

Flask API (app.py):

Accepts POST requests with plain text, URLs, or image files.
Uses OCR for image input via Tesseract.
Parses article content from URLs using newspaper3k.
Returns prediction and confidence level.


Setup Instructions:
Prerequisites
Python 3.7+
Google Chrome
Tesseract OCR (for image-based detection)
