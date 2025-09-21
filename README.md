# -AI-Powered-Tool-for-Combating-Misinformation
This AI-powered browser extension helps users detect and verify misinformation online. It uses AI algorithms to fact-check text, images, and sources, cross-references content with trusted websites, and incorporates community feedback to flag suspicious information.


FAKE-NEWS-DETECTOR/
│
├── fake_news_extensions/      # Chrome extension files
│   ├── icon.png               # Extension icon
│   ├── manifest.json          # Chrome extension manifest (v3)
│   ├── popup.html             # Extension UI
│   ├── popup.js               # Client-side JS logic
│   └── style.css              # Styles for the popup
│
├── Model/                     # ML model and tokenizer
│   ├── lstm_model.keras       # Trained LSTM model
│   └── tokenizer.pkl          # Tokenizer for preprocessing
│
├── templates/
│   └── index.html             # Web interface (Flask-based)
│
├── app.py                     # Flask backend with REST API
├── README.md                  # Project documentation
