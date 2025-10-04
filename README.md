# FactScope - AI-Powered Fake News Detector

A full-stack web application that uses AI and natural language processing to detect fake news articles, verify headlines, and analyze content credibility.

##  Features

- **URL Analysis**: Scrapes and analyzes news articles from URLs
- **Headline Verification**: Checks headlines for clickbait and sensational language
- **Domain Reputation**: Evaluates source credibility
- **AI-Powered Detection**: Uses pattern matching and heuristics to identify misinformation
- **Confidence Scoring**: Provides percentage-based confidence levels
- **Interactive Results**: Shows detailed analysis with follow-up options
- **Beautiful UI**: Modern, responsive design with gradient backgrounds

##  Quick Start

### 1. Install Dependencies
```bash
pip3 install Flask flask-cors requests beautifulsoup4 lxml Pillow
```

### 2. Start the Backend
```bash
./start_backend.sh
```
Or manually:
```bash
python3 app.py
```

The backend will start on **http://localhost:5001**

### 3. Open the Frontend
Simply open `index.html` in your web browser:
- Double-click the file, or
- Right-click → Open with → Browser

##  How to Use

1. **Enter News Information**:
   - Paste a news article URL
   - Type a headline to verify
   - Upload a news image (optional)

2. **Click "Verify News"**:
   - The system analyzes the content
   - Results appear in three categories:
     -  **Fully True** (Green)
     -  **Partially True** (Orange)
     -  **Fully False** (Red)

3. **View Details**:
   - Click "Show Summary" for context
   - Click "Show Reason" to understand the analysis

##  Technical Details

### Backend (Flask API)
- **Framework**: Flask with CORS support
- **Web Scraping**: BeautifulSoup4 for content extraction
- **Analysis Engine**: Pattern matching and heuristic-based detection
- **Endpoints**:
  - `POST /api/verify` - Verify news content
  - `GET /api/health` - Health check

### Frontend
- **HTML5** with semantic markup
- **CSS3** with modern gradients and animations
- **Vanilla JavaScript** for API integration
- **Responsive Design** for all devices

### Detection Algorithm
The system analyzes multiple factors:
- Sensational language patterns
- Clickbait indicators
- Credible source references
- Domain reputation
- Writing style analysis
- Punctuation and capitalization patterns

##  Project Structure

```
Prompt-Pandemic-restinPython/
├── app.py                    # Flask backend server
├── script.js                 # Frontend JavaScript
├── index.html                # Main HTML page
├── style.css                 # Styling
├── requirements.txt          # Python dependencies
├── start_backend.sh          # Quick start script
├── SETUP_INSTRUCTIONS.md     # Detailed setup guide
└── README.md                 # This file
```

##  Testing

Test the API directly:
```bash
curl -X POST http://localhost:5001/api/verify \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news/example", "headline": "Breaking News"}'
```

##  Example Usage

**Test with a credible source:**
- URL: `https://www.bbc.com/news/world`
- Expected: High credibility score

**Test with sensational headline:**
- Headline: "You won't believe what happened next! SHOCKING!!!"
- Expected: Low credibility, flagged as potentially false

##  Configuration

To change the port, edit `app.py`:
```python
app.run(debug=True, port=5001)  # Change port here
```

And update `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001/api';  // Match the port
```

##  Credibility Indicators

**Positive Indicators:**
- References to studies and research
- Credible source citations
- Balanced reporting
- Known reputable domains

**Negative Indicators:**
- Excessive sensational language
- Clickbait patterns
- Lack of sources
- Excessive punctuation/caps
- Unknown or suspicious domains

##  Limitations

- Heuristic-based (not deep learning)
- Limited domain reputation database
- English language optimized
- Some websites block scraping
- Image analysis requires external APIs

##  Future Enhancements

- [ ] Integration with fact-checking APIs
- [ ] Machine learning model training
- [ ] OCR for image text extraction
- [ ] Reverse image search
- [ ] Multi-language support
- [ ] User feedback system
- [ ] Historical tracking database
- [ ] Browser extension

##  API Documentation

### POST /api/verify

**Request:**
```json
{
  "url": "https://example.com/article",
  "headline": "News headline",
  "image": "base64_encoded_image"
}
```

**Response:**
```json
{
  "overall": {
    "credibility": "partial",
    "confidence": 75.0
  },
  "analysis": {
    "url": {
      "credibility": "partial",
      "confidence": 75.0,
      "title": "Article Title",
      "domain": "example.com",
      "domain_reputation": "unknown",
      "indicators": {...},
      "summary": "Analysis summary",
      "reason": "Detailed reasoning"
    }
  }
}
```

##  Troubleshooting

**Backend not starting:**
- Check if port 5001 is available
- Ensure all dependencies are installed
- Check Python version (3.8+)

**CORS errors:**
- Make sure backend is running
- Check browser console for details
- Verify API_BASE_URL in script.js

**Article extraction fails:**
- Some sites block scraping
- Try different news sources
- Check internet connection

##  License

 2025 Fact@Scope.pvt.ltd All Rights Reserved

##  Support

For issues or questions:
1. Check the console logs
2. Review SETUP_INSTRUCTIONS.md
3. Verify backend is running: `curl http://localhost:5001/api/health`

---

**Built with  using Flask, JavaScript, and AI**inPython
