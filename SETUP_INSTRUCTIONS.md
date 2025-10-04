# Fake News Detector - Setup Instructions

## Overview
This is a full-stack fake news detection application with:
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python) with AI-powered analysis
- **Features**: URL analysis, headline verification, domain reputation checking

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask flask-cors requests beautifulsoup4 Pillow lxml
```

### 2. Start the Backend Server
```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 3. Open the Frontend
Open `index.html` in your web browser:
- Double-click the file, or
- Right-click → Open with → Your browser, or
- Use a local server (recommended):
  ```bash
  python -m http.server 8000
  ```
  Then visit `http://localhost:8000`

## How to Use

### 1. Enter News Information
You can provide any combination of:
- **News URL**: Paste the full URL of a news article
- **News Headline**: Type or paste a headline
- **News Image**: Upload a screenshot (basic support)

### 2. Click "Verify News"
The system will analyze the content and display results in three categories:
- **Fully True** (Green): Credible content with reliable sources
- **Partially True** (Orange): Mixed credibility, needs verification
- **Fully False** (Red): High indicators of misinformation

### 3. View Details
- For **Partially True** news: Click "Show Summary" for context
- For **Fully False** news: Click "Show Reason" to understand why

## How It Works

### Backend Analysis (`app.py`)
1. **URL Analysis**:
   - Extracts article content using web scraping
   - Analyzes text for fake news indicators
   - Checks domain reputation

2. **Credibility Indicators**:
   - Sensational language detection
   - Clickbait pattern recognition
   - Credible source references
   - Excessive punctuation/capitalization
   - Domain reputation scoring

3. **Scoring Algorithm**:
   - Combines multiple indicators
   - Weights domain reputation
   - Calculates confidence percentage

### Frontend (`script.js`)
- Sends requests to Flask API
- Displays results dynamically
- Provides interactive follow-up options

## API Endpoints

### POST `/api/verify`
Verify news content
```json
{
  "url": "https://example.com/article",
  "headline": "Breaking News Title",
  "image": "base64_encoded_image"
}
```

Response:
```json
{
  "overall": {
    "credibility": "true|partial|false",
    "confidence": 85.5
  },
  "analysis": {
    "url": {
      "credibility": "partial",
      "confidence": 75.0,
      "title": "Article Title",
      "domain": "example.com",
      "domain_reputation": "unknown",
      "summary": "...",
      "reason": "..."
    }
  }
}
```

### GET `/api/health`
Check API status
```json
{
  "status": "healthy",
  "service": "Fake News Detector API"
}
```

## Troubleshooting

### Backend not responding
- Make sure Flask is running: `python app.py`
- Check port 5000 is not in use
- Look for error messages in terminal

### CORS errors
- The backend includes CORS support
- If issues persist, check browser console

### Article extraction fails
- Some websites block scraping
- Try with different news sources
- Check internet connection

## Limitations

1. **Heuristic-based**: Uses pattern matching, not deep learning
2. **Domain list**: Limited to common sources
3. **Image analysis**: Basic support (requires external OCR/vision APIs for full functionality)
4. **Language**: Optimized for English content

## Future Enhancements

- Integration with fact-checking APIs (FactCheck.org, Snopes)
- Machine learning model for better accuracy
- OCR for image text extraction
- Reverse image search integration
- Multi-language support
- User feedback system
- Historical tracking

## Tech Stack

- **Backend**: Flask, BeautifulSoup, Requests
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Analysis**: Pattern matching, domain reputation, text analysis

## License
© 2025 Fact@Scope.pvt.ltd All Rights Reserved

## Support
For issues or questions, check the console logs for detailed error messages.
