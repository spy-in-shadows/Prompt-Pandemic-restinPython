from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import base64
from io import BytesIO
from PIL import Image
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://spy-in-shadows.github.io"}})

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to extract article content from URL
def extract_article_content(url):
    """Extract article text from a news URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=3)  # Reduced to 3 seconds
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find article content
        article_text = ""
        
        # Common article selectors
        article_selectors = [
            'article', '.article-content', '.post-content', 
            '.entry-content', '.article-body', 'main'
        ]
        
        for selector in article_selectors:
            article = soup.select_one(selector)
            if article:
                article_text = article.get_text(separator=' ', strip=True)
                break
        
        # Fallback to paragraphs
        if not article_text:
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        
        # Get title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else ""
        
        # Clean text
        article_text = re.sub(r'\s+', ' ', article_text).strip()
        
        return {
            'title': title_text,
            'content': article_text[:5000],  # Limit content length
            'url': url,
            'domain': urlparse(url).netloc
        }
    except Exception as e:
        return {'error': f'Failed to extract content: {str(e)}'}

# Helper function to analyze text credibility
def analyze_text_credibility(text, headline=""):
    """Analyze text for fake news indicators using heuristics and patterns"""
    
    # Combine headline and text
    full_text = f"{headline} {text}".lower()
    
    # High-risk sensational words (weight: 2 points each)
    high_risk_words = [
        'shocking', 'unbelievable', 'miracle', 'secret', 'exposed',
        'scandal', 'conspiracy', 'bombshell', 'explosive', 'leaked'
    ]
    
    # Medium-risk sensational words (weight: 1 point each)
    medium_risk_words = [
        'breaking', 'urgent', 'alert', 'exclusive', 'revealed',
        'truth', 'hidden', 'banned', 'censored', 'forbidden'
    ]
    
    # Clickbait patterns (weight: 3 points each - very strong indicator)
    clickbait_patterns = [
        r'you wo?n[\'t]? believe',  # Matches "won't", "wont", "won t"
        r'what happened next',
        r'number \d+ will shock',
        r'this one trick',
        r'\d+ reasons? why',
        r'doctors hate',
        r'they don[\'t]? want you to know',
        r'what they[\'r]?e hiding',
        r'the truth about',
        r'will blow your mind'
    ]
    
    # Credibility indicators (positive signals)
    credibility_indicators = [
        'study shows', 'research indicates', 'according to',
        'experts say', 'data suggests', 'published in',
        'university', 'institute', 'professor', 'peer-reviewed',
        'journal', 'scientists', 'researchers found'
    ]
    
    # Calculate scores with weights
    high_risk_score = sum(2 for word in high_risk_words if word in full_text)
    medium_risk_score = sum(1 for word in medium_risk_words if word in full_text)
    clickbait_score = sum(3 for pattern in clickbait_patterns if re.search(pattern, full_text))
    credibility_score = sum(1 for indicator in credibility_indicators if indicator in full_text)
    
    # Check for excessive punctuation (weight: 2 points each)
    excessive_punctuation = len(re.findall(r'[!?]{2,}', full_text + headline))
    punctuation_score = excessive_punctuation * 2
    
    # Check for all caps words (shouting) (weight: 1.5 points each)
    caps_words = len(re.findall(r'\b[A-Z]{3,}\b', headline + " " + text))
    caps_score = int(caps_words * 1.5)
    
    # Total negative score (weighted)
    # Don't count caps if there are strong credibility indicators (legitimate breaking news)
    if credibility_score >= 2:
        # Reduce caps penalty for credible sources
        caps_score = int(caps_score * 0.3)
    
    negative_score = high_risk_score + medium_risk_score + clickbait_score + punctuation_score + caps_score
    positive_score = credibility_score
    
    # Improved scoring algorithm with credibility override
    # If strong credibility indicators exist, be more lenient
    if positive_score >= 3:
        # Strong credibility - likely true even with some negative signals
        credibility = 'true'
        confidence = min(75 + positive_score * 4, 92)
    # FALSE: Clickbait patterns are strong indicators
    elif clickbait_score > 0:
        if positive_score == 0:
            credibility = 'false'
            confidence = min(80 + negative_score * 3, 98)
        else:
            # Has credibility but also clickbait - mixed
            credibility = 'partial'
            confidence = min(65 + (negative_score - positive_score) * 2, 80)
    # FALSE: High negative score with no credibility
    elif negative_score >= 6 and positive_score == 0:
        credibility = 'false'
        confidence = min(75 + negative_score * 3, 95)
    # PARTIAL: High negative with some credibility OR moderate negative
    elif negative_score >= 4 and positive_score > 0:
        credibility = 'partial'
        confidence = 60 + abs(positive_score - negative_score) * 3
        confidence = min(max(confidence, 55), 80)
    # PARTIAL: Moderate negative or mixed signals
    elif negative_score >= 3 or (negative_score > 0 and positive_score > 0):
        credibility = 'partial'
        confidence = 55 + abs(positive_score - negative_score) * 4
        confidence = min(max(confidence, 50), 75)
    # TRUE: Strong positive indicators
    elif positive_score >= 2:
        credibility = 'true'
        confidence = min(70 + positive_score * 5, 90)
    # NEUTRAL/TRUE: No strong signals either way
    else:
        if negative_score == 0:
            credibility = 'true'
            confidence = 65
        elif negative_score <= 2:
            credibility = 'partial'
            confidence = 60
        else:
            credibility = 'partial'
            confidence = 55
    
    # Count raw occurrences for display
    sensational_count = sum(1 for word in high_risk_words + medium_risk_words if word in full_text)
    clickbait_count = sum(1 for pattern in clickbait_patterns if re.search(pattern, full_text))
    
    return {
        'credibility': credibility,
        'confidence': round(confidence, 1),
        'indicators': {
            'sensational_words': sensational_count,
            'clickbait_patterns': clickbait_count,
            'credibility_indicators': credibility_score,
            'excessive_punctuation': excessive_punctuation,
            'caps_words': caps_words
        }
    }

# Helper function to check domain reputation
def check_domain_reputation(domain):
    """Check if domain is known for fake news or credible journalism"""
    
    # Known credible sources
    credible_domains = [
        'bbc.com', 'reuters.com', 'apnews.com', 'npr.org',
        'nytimes.com', 'washingtonpost.com', 'theguardian.com',
        'cnn.com', 'bloomberg.com', 'wsj.com', 'economist.com',
        'nature.com', 'science.org', 'scientificamerican.com'
    ]
    
    # Known unreliable sources (simplified list)
    unreliable_domains = [
        'fake', 'hoax', 'satire', 'parody', 'conspiracy'
    ]
    
    domain_lower = domain.lower()
    
    # Check credible
    for credible in credible_domains:
        if credible in domain_lower:
            return {'reputation': 'credible', 'score': 90}
    
    # Check unreliable
    for unreliable in unreliable_domains:
        if unreliable in domain_lower:
            return {'reputation': 'unreliable', 'score': 10}
    
    # Unknown domain
    return {'reputation': 'unknown', 'score': 50}

@app.route('/api/verify', methods=['POST'])
def verify_news():
    """Main endpoint to verify news"""
    try:
        data = request.get_json()
        
        news_url = data.get('url', '').strip()
        news_headline = data.get('headline', '').strip()
        news_image = data.get('image')  # Base64 encoded image
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'analysis': {}
        }
        
        # Analyze URL if provided
        if news_url:
            article_data = extract_article_content(news_url)
            
            if 'error' not in article_data:
                # Check if content is empty or too short (likely no real content found)
                content_length = len(article_data['content'].strip())
                
                if content_length < 50:
                    # No meaningful content found - mark as not true
                    results['analysis']['url'] = {
                        'credibility': 'false',
                        'confidence': 75.0,
                        'title': article_data['title'] or 'No title found',
                        'domain': article_data['domain'],
                        'domain_reputation': 'unknown',
                        'indicators': {
                            'sensational_words': 0,
                            'clickbait_patterns': 0,
                            'credibility_indicators': 0,
                            'excessive_punctuation': 0,
                            'caps_words': 0
                        },
                        'summary': 'No verifiable content found from trusted sources.',
                        'reason': 'Unable to extract meaningful content from the URL. The information could not be verified against trusted sources.'
                    }
                else:
                    # Analyze content
                    text_analysis = analyze_text_credibility(
                        article_data['content'],
                        article_data['title']
                    )
                    
                    # Check domain
                    domain_check = check_domain_reputation(article_data['domain'])
                    
                    # Combine analyses
                    final_credibility = text_analysis['credibility']
                    final_confidence = text_analysis['confidence']
                    
                    # Adjust based on domain reputation
                    if domain_check['reputation'] == 'credible':
                        if final_credibility == 'false':
                            final_credibility = 'partial'
                        final_confidence = min((final_confidence + domain_check['score']) / 2, 95)
                    elif domain_check['reputation'] == 'unreliable':
                        final_credibility = 'false'
                        final_confidence = max(final_confidence, 75)
                    
                    results['analysis']['url'] = {
                        'credibility': final_credibility,
                        'confidence': round(final_confidence, 1),
                        'title': article_data['title'],
                        'domain': article_data['domain'],
                        'domain_reputation': domain_check['reputation'],
                        'indicators': text_analysis['indicators'],
                        'summary': generate_summary(article_data['content'], final_credibility),
                        'reason': generate_reason(final_credibility, text_analysis['indicators'])
                    }
            else:
                # Error extracting content - mark as not true
                results['analysis']['url'] = {
                    'credibility': 'false',
                    'confidence': 70.0,
                    'title': 'Unable to access URL',
                    'domain': urlparse(news_url).netloc if news_url else 'unknown',
                    'domain_reputation': 'unknown',
                    'indicators': {
                        'sensational_words': 0,
                        'clickbait_patterns': 0,
                        'credibility_indicators': 0,
                        'excessive_punctuation': 0,
                        'caps_words': 0
                    },
                    'summary': 'Unable to verify this information from trusted sources.',
                    'reason': f'Could not access or verify the content. {article_data.get("error", "Unknown error")}'
                }
        
        # Analyze headline if provided
        if news_headline:
            headline_analysis = analyze_text_credibility("", news_headline)
            
            results['analysis']['headline'] = {
                'credibility': headline_analysis['credibility'],
                'confidence': round(headline_analysis['confidence'], 1),
                'text': news_headline,
                'indicators': headline_analysis['indicators'],
                'reason': generate_reason(headline_analysis['credibility'], headline_analysis['indicators'])
            }
        
        # Handle image if provided
        if news_image:
            results['analysis']['image'] = {
                'status': 'received',
                'note': 'Image analysis requires additional AI services (OCR, reverse image search)',
                'credibility': 'unknown',
                'confidence': 0
            }
        
        # Determine overall result
        if 'url' in results['analysis']:
            overall = results['analysis']['url']
        elif 'headline' in results['analysis']:
            overall = results['analysis']['headline']
        else:
            return jsonify({'error': 'No valid input provided'}), 400
        
        results['overall'] = {
            'credibility': overall['credibility'],
            'confidence': overall['confidence']
        }
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_summary(content, credibility):
    """Generate a summary based on content and credibility"""
    if credibility == 'true':
        return "This article appears to contain factual information with credible sources and balanced reporting."
    elif credibility == 'partial':
        return "This article contains some factual information but may lack context, use sensational language, or mix facts with opinion. Verify key claims with additional sources."
    else:
        return "This article shows multiple indicators of misinformation, including sensational language, lack of credible sources, and potentially misleading claims. Exercise caution and verify with trusted sources."

def generate_reason(credibility, indicators):
    """Generate reason for the credibility assessment"""
    reasons = []
    
    if indicators['sensational_words'] > 2:
        reasons.append("Contains excessive sensational language")
    
    if indicators['clickbait_patterns'] > 0:
        reasons.append("Uses clickbait-style headlines")
    
    if indicators['excessive_punctuation'] > 0:
        reasons.append("Uses excessive punctuation for emphasis")
    
    if indicators['caps_words'] > 2:
        reasons.append("Contains excessive capitalization")
    
    if indicators['credibility_indicators'] > 2:
        reasons.append("References credible sources and research")
    
    if not reasons:
        if credibility == 'true':
            reasons.append("Appears to follow journalistic standards")
        else:
            reasons.append("Lacks clear credibility indicators")
    
    return "; ".join(reasons)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Fake News Detector API'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
