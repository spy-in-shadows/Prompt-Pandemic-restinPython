// API Configuration
const API_BASE_URL = 'https://prompt-pandemic-restinpython.onrender.com';

// Get DOM elements
const newsForm = document.getElementById('news-form');
const resultsSection = document.getElementById('results-section');
const followupSection = document.getElementById('followup-section');
const trueList = document.getElementById('true-list');
const partialList = document.getElementById('partial-list');
const falseList = document.getElementById('false-list');
const summaryOption = document.getElementById('summary-option');
const reasonOption = document.getElementById('reason-option');
const outputDetails = document.getElementById('output-details');
const showSummaryBtn = document.getElementById('show-summary');
const showReasonBtn = document.getElementById('show-reason');

// Store current analysis results
let currentAnalysis = null;

// Form submission handler
newsForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form values
    const newsUrl = document.getElementById('news-url').value.trim();
    const newsHeadline = document.getElementById('news-headline').value.trim();
    const newsImageFile = document.getElementById('news-image').files[0];
    
    // Validate input
    if (!newsUrl && !newsHeadline && !newsImageFile) {
        alert('Please provide at least one input: URL, headline, or image.');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        // Prepare request data
        const requestData = {
            url: newsUrl,
            headline: newsHeadline
        };
        
        // Handle image if provided
        if (newsImageFile) {
            const imageBase64 = await fileToBase64(newsImageFile);
            requestData.image = imageBase64;
        }
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        currentAnalysis = data;
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Error verifying news: ${error.message}\n\nMake sure the Flask backend is running on port 5000.`);
        hideLoading();
    }
});

// Show summary button handler
showSummaryBtn.addEventListener('click', function() {
    if (currentAnalysis && currentAnalysis.analysis.url) {
        const summary = currentAnalysis.analysis.url.summary;
        outputDetails.innerHTML = `<p><strong>Summary:</strong> ${summary}</p>`;
        outputDetails.style.display = 'block';
    }
});

// Show reason button handler
showReasonBtn.addEventListener('click', function() {
    if (currentAnalysis) {
        let reason = '';
        if (currentAnalysis.analysis.url) {
            reason = currentAnalysis.analysis.url.reason;
        } else if (currentAnalysis.analysis.headline) {
            reason = currentAnalysis.analysis.headline.reason;
        }
        
        outputDetails.innerHTML = `<p><strong>Reason:</strong> ${reason}</p>`;
        outputDetails.style.display = 'block';
    }
});

// Helper function to convert file to base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Show loading state
function showLoading() {
    // Clear previous results
    trueList.innerHTML = '<li>Analyzing...</li>';
    partialList.innerHTML = '';
    falseList.innerHTML = '';
    
    resultsSection.style.display = 'block';
    followupSection.style.display = 'none';
    outputDetails.innerHTML = '';
    outputDetails.style.display = 'none';
}

// Hide loading state
function hideLoading() {
    resultsSection.style.display = 'none';
}

// Display results
function displayResults(data) {
    // Clear previous results
    trueList.innerHTML = '';
    partialList.innerHTML = '';
    falseList.innerHTML = '';
    
    // Get the main analysis (prioritize URL over headline)
    let mainAnalysis = null;
    let analysisType = '';
    
    if (data.analysis.url) {
        mainAnalysis = data.analysis.url;
        analysisType = 'URL';
    } else if (data.analysis.headline) {
        mainAnalysis = data.analysis.headline;
        analysisType = 'Headline';
    }
    
    if (!mainAnalysis) {
        alert('No analysis results available.');
        return;
    }
    
    // Create result item
    const resultText = createResultText(mainAnalysis, analysisType);
    
    // Determine section based on confidence level and credibility
    let finalCredibility = mainAnalysis.credibility;
    
    // Classify based on confidence levels
    if (mainAnalysis.confidence >= 80) {
        // High confidence: use the credibility as-is (true stays true, false stays false)
        if (mainAnalysis.credibility === 'partial') {
            finalCredibility = 'true';  // Upgrade partial to true with high confidence
        }
    } else if (mainAnalysis.confidence > 50 && mainAnalysis.confidence < 80) {
        // Medium confidence: classify as partially true
        finalCredibility = 'partial';
    }
    // If confidence <= 50, keep original credibility
    
    // Add to appropriate list based on final credibility
    if (finalCredibility === 'true') {
        trueList.innerHTML = `<li>${resultText}</li>`;
    } else if (finalCredibility === 'partial') {
        partialList.innerHTML = `<li>${resultText}</li>`;
    } else if (finalCredibility === 'false') {
        falseList.innerHTML = `<li>${resultText}</li>`;
    }
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Show follow-up options based on final credibility
    showFollowupOptions(finalCredibility);
}

// Create result text
function createResultText(analysis, type) {
    let text = '';
    
    if (type === 'URL') {
        text = `<strong>${analysis.title || 'Article'}</strong><br>`;
        text += `Domain: ${analysis.domain}<br>`;
        text += `Domain Reputation: ${analysis.domain_reputation}<br>`;
    } else if (type === 'Headline') {
        text = `<strong>${analysis.text}</strong><br>`;
    }
    
    text += `Confidence: ${analysis.confidence}%<br>`;
    
    // Add indicators
    if (analysis.indicators) {
        const indicators = analysis.indicators;
        text += '<br><strong>Analysis Indicators:</strong><br>';
        
        if (indicators.sensational_words > 0) {
            text += `• Sensational words detected: ${indicators.sensational_words}<br>`;
        }
        if (indicators.clickbait_patterns > 0) {
            text += `• Clickbait patterns detected: ${indicators.clickbait_patterns}<br>`;
        }
        if (indicators.credibility_indicators > 0) {
            text += `• Credibility indicators found: ${indicators.credibility_indicators}<br>`;
        }
        if (indicators.excessive_punctuation > 0) {
            text += `• Excessive punctuation detected<br>`;
        }
        if (indicators.caps_words > 0) {
            text += `• Excessive capitalization detected<br>`;
        }
    }
    
    return text;
}

// Show follow-up options
function showFollowupOptions(credibility) {
    followupSection.style.display = 'block';
    summaryOption.style.display = 'none';
    reasonOption.style.display = 'none';
    outputDetails.innerHTML = '';
    outputDetails.style.display = 'none';
    
    if (credibility === 'partial') {
        summaryOption.style.display = 'block';
    } else if (credibility === 'false') {
        reasonOption.style.display = 'block';
    } else if (credibility === 'true') {
        summaryOption.style.display = 'block';
    }
}

// Check backend health on page load
window.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('Backend API is healthy');
        }
    } catch (error) {
        console.warn('Backend API is not responding. Make sure Flask server is running on port 5000.');
    }
});
