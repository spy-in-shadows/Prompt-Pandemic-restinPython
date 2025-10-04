# Test Examples for Fake News Detector

## Example 1: Clickbait Headline (Should be flagged as FALSE)

**Test Input:**
```
Headline: "You won't believe what happened next! SHOCKING news!!!"
```

**Expected Result:**
- Credibility: FALSE
- High confidence (85-95%)
- Indicators: Clickbait patterns, excessive punctuation, sensational words

**Test Command:**
```bash
curl -X POST http://localhost:5001/api/verify \
  -H "Content-Type: application/json" \
  -d '{"headline": "You wont believe what happened next! SHOCKING news!!!"}'
```

---

## Example 2: Credible Headline (Should be TRUE or PARTIAL)

**Test Input:**
```
Headline: "Study shows climate change impacts coastal regions, according to research published in Nature"
```

**Expected Result:**
- Credibility: TRUE or PARTIAL
- Moderate to high confidence
- Indicators: References to studies, credible sources

**Test Command:**
```bash
curl -X POST http://localhost:5001/api/verify \
  -H "Content-Type: application/json" \
  -d '{"headline": "Study shows climate change impacts coastal regions, according to research published in Nature"}'
```

---

## Example 3: URL Analysis (Credible Source)

**Test Input:**
```
URL: https://www.bbc.com/news
```

**Expected Result:**
- Domain reputation: CREDIBLE
- Higher confidence score
- Balanced analysis

**Test Command:**
```bash
curl -X POST http://localhost:5001/api/verify \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news"}'
```

---

## Example 4: Sensational Language

**Test Input:**
```
Headline: "BREAKING: URGENT ALERT! Miracle cure EXPOSED! Doctors HATE this!"
```

**Expected Result:**
- Credibility: FALSE
- Very high confidence (90%+)
- Multiple indicators: Sensational words, caps, clickbait

**Test Command:**
```bash
curl -X POST http://localhost:5001/api/verify \
  -H "Content-Type: application/json" \
  -d '{"headline": "BREAKING: URGENT ALERT! Miracle cure EXPOSED! Doctors HATE this!"}'
```

---

## Example 5: Neutral News

**Test Input:**
```
Headline: "Local council approves new infrastructure project"
```

**Expected Result:**
- Credibility: TRUE or PARTIAL
- Moderate confidence
- Few indicators detected

**Test Command:**
```bash
curl -X POST http://localhost:5001/api/verify \
  -H "Content-Type: application/json" \
  -d '{"headline": "Local council approves new infrastructure project"}'
```

---

## Testing via Web Interface

1. Open `index.html` in your browser
2. Try these test cases:

### Test Case 1: Fake News
- **Headline**: "You won't believe this shocking secret they don't want you to know!!!"
- **Expected**: Red (Fully False) with reason shown

### Test Case 2: Real News
- **URL**: https://www.reuters.com/world/
- **Expected**: Green (Fully True) or Orange (Partially True)

### Test Case 3: Mixed
- **Headline**: "Breaking: Study suggests new findings on health"
- **Expected**: Orange (Partially True) - has "breaking" but also "study"

---

## Interpreting Results

### Credibility Levels:
- **TRUE**: Low negative indicators, high credibility markers
- **PARTIAL**: Mixed signals, needs verification
- **FALSE**: High negative indicators, low credibility

### Confidence Score:
- **90-100%**: Very confident in assessment
- **70-89%**: Confident with some uncertainty
- **50-69%**: Moderate confidence, borderline case
- **Below 50%**: Low confidence, needs human review

### Key Indicators:
1. **Sensational Words**: shocking, unbelievable, miracle, exposed
2. **Clickbait Patterns**: "you won't believe", "what happened next"
3. **Credibility Indicators**: study, research, according to, experts
4. **Excessive Punctuation**: Multiple !!! or ???
5. **Caps Words**: BREAKING, URGENT, SHOCKING

---

## Notes

- The system uses heuristic analysis, not deep learning
- Results are based on patterns and indicators
- Always verify important news with multiple sources
- Domain reputation affects final scoring
- Some legitimate breaking news may trigger false positives
