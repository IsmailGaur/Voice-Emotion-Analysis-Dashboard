# 📡 API Documentation

Complete API reference for the Voice Emotion Analysis application.

## Base URL

- **Local**: `http://localhost:5000`
- **Production**: `https://your-app.onrender.com`

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy"
}
```

**Status Codes**:
- `200 OK`: Service is running

**Example**:
```bash
curl http://localhost:5000/health
```

---

### 2. Analyze Audio

Upload and analyze an audio file for emotion detection.

**Endpoint**: `POST /analyze`

**Content-Type**: `multipart/form-data`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| audio | file | Yes | Audio file (WAV, MP3, FLAC, OGG, M4A) |

**Request Example**:

```bash
curl -X POST http://localhost:5000/analyze \
  -F "audio=@path/to/audio.wav"
```

**Success Response**:

```json
{
  "success": true,
  "results": [
    {
      "start_time": 0.0,
      "end_time": 3.0,
      "emotion": "neutral",
      "confidence": 0.8523,
      "all_scores": {
        "angry": 0.0234,
        "calm": 0.0456,
        "disgust": 0.0123,
        "fearful": 0.0342,
        "happy": 0.0543,
        "neutral": 0.8523,
        "sad": 0.0234,
        "surprised": 0.0345
      }
    },
    {
      "start_time": 3.0,
      "end_time": 6.0,
      "emotion": "happy",
      "confidence": 0.7891,
      "all_scores": {
        "angry": 0.0123,
        "calm": 0.0234,
        "disgust": 0.0098,
        "fearful": 0.0234,
        "happy": 0.7891,
        "neutral": 0.1234,
        "sad": 0.0098,
        "surprised": 0.0088
      }
    }
  ],
  "emotion_changes": [
    {
      "timestamp": 3.0,
      "from_emotion": "neutral",
      "to_emotion": "happy",
      "confidence": 0.7891
    }
  ],
  "statistics": {
    "total_duration": 15.0,
    "emotion_counts": {
      "neutral": 2,
      "happy": 3
    },
    "emotion_durations": {
      "neutral": 6.0,
      "happy": 9.0
    },
    "emotion_percentages": {
      "neutral": 40.0,
      "happy": 60.0
    },
    "dominant_emotion": "happy"
  }
}
```

**Error Response**:

```json
{
  "error": "No audio file provided"
}
```

**Status Codes**:
- `200 OK`: Analysis successful
- `400 Bad Request`: Invalid request (missing file, wrong format)
- `500 Internal Server Error`: Server error during processing

---

### 3. Dashboard

Get the main dashboard HTML page.

**Endpoint**: `GET /`

**Response**: HTML page

**Status Codes**:
- `200 OK`: Page loaded successfully

---

## Response Objects

### Result Object

Each audio chunk analyzed returns:

```typescript
{
  start_time: number,      // Start timestamp in seconds
  end_time: number,        // End timestamp in seconds
  emotion: string,         // Predicted emotion
  confidence: number,      // Confidence score (0-1)
  all_scores: {           // Scores for all emotions
    [emotion: string]: number
  }
}
```

### Emotion Change Object

```typescript
{
  timestamp: number,           // When emotion changed (seconds)
  from_emotion: string,        // Previous emotion
  to_emotion: string,          // New emotion
  confidence: number           // Confidence of new emotion
}
```

### Statistics Object

```typescript
{
  total_duration: number,                    // Total audio duration
  emotion_counts: {                          // Count of chunks per emotion
    [emotion: string]: number
  },
  emotion_durations: {                       // Total time per emotion
    [emotion: string]: number
  },
  emotion_percentages: {                     // Percentage per emotion
    [emotion: string]: number
  },
  dominant_emotion: string                   // Most frequent emotion
}
```

---

## Emotion Labels

The API detects the following emotions:

| Emotion | Description | Typical Characteristics |
|---------|-------------|------------------------|
| angry | Anger, frustration | High energy, elevated pitch |
| calm | Calmness, peace | Low energy, stable pitch |
| disgust | Disgust, distaste | Specific vocal patterns |
| fearful | Fear, anxiety | High pitch variability |
| happy | Happiness, joy | High energy, varied pitch |
| neutral | Neutral state | Moderate characteristics |
| sad | Sadness, sorrow | Low energy, low pitch |
| surprised | Surprise, shock | Sudden pitch changes |

---

## Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | NO_FILE | No audio file in request |
| 400 | EMPTY_FILE | File name is empty |
| 400 | INVALID_FORMAT | File format not supported |
| 400 | FILE_TOO_LARGE | File exceeds size limit (50MB) |
| 500 | PROCESSING_ERROR | Error during audio processing |
| 500 | MODEL_ERROR | Error in emotion detection model |

---

## Rate Limits

Currently no rate limits are enforced. In production, consider:

- 10 requests per minute per IP
- 100 requests per hour per IP

---

## File Constraints

- **Maximum file size**: 50 MB
- **Supported formats**: WAV, MP3, FLAC, OGG, M4A
- **Recommended**: 
  - Sample rate: 16kHz or 44.1kHz
  - Mono channel
  - Duration: 10 seconds - 5 minutes

---

## Processing Time

Processing time varies by file length:

| Audio Length | Approx. Processing Time |
|--------------|------------------------|
| 10 seconds   | 3-5 seconds |
| 30 seconds   | 10-15 seconds |
| 1 minute     | 20-30 seconds |
| 5 minutes    | 2-3 minutes |

*Times based on CPU processing on average hardware*

---

## Code Examples

### Python

```python
import requests

# Upload and analyze audio
url = 'http://localhost:5000/analyze'
files = {'audio': open('audio.wav', 'rb')}

response = requests.post(url, files=files)
data = response.json()

if data['success']:
    print(f"Dominant emotion: {data['statistics']['dominant_emotion']}")
    for result in data['results']:
        print(f"{result['start_time']:.1f}s - {result['emotion']}")
else:
    print(f"Error: {data['error']}")
```

### JavaScript (Node.js)

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('audio', fs.createReadStream('audio.wav'));

axios.post('http://localhost:5000/analyze', form, {
  headers: form.getHeaders()
})
.then(response => {
  const data = response.data;
  if (data.success) {
    console.log(`Dominant emotion: ${data.statistics.dominant_emotion}`);
    data.results.forEach(result => {
      console.log(`${result.start_time}s - ${result.emotion}`);
    });
  }
})
.catch(error => console.error('Error:', error));
```

### cURL

```bash
# Basic analysis
curl -X POST http://localhost:5000/analyze \
  -F "audio=@audio.wav"

# Save response to file
curl -X POST http://localhost:5000/analyze \
  -F "audio=@audio.wav" \
  -o results.json

# Pretty print JSON
curl -X POST http://localhost:5000/analyze \
  -F "audio=@audio.wav" \
  | python -m json.tool
```

---

## Webhook Support

Currently not implemented. Future versions may support webhooks for:

- Completion notifications
- Real-time emotion updates
- Error alerts

---

## Authentication

Currently no authentication required. For production:

1. Add API key authentication
2. Implement OAuth 2.0
3. Use JWT tokens

Example with API key:

```python
headers = {'X-API-Key': 'your-api-key'}
response = requests.post(url, files=files, headers=headers)
```

---

## CORS

CORS is enabled by default. To customize:

```python
from flask_cors import CORS

CORS(app, origins=['https://yourdomain.com'])
```

---

## Versioning

Current version: `1.0.0`

Future API versions will use URL versioning:
- `/v1/analyze`
- `/v2/analyze`

---

## Support

For API issues:
1. Check response error messages
2. Verify file format and size
3. Test with sample audio files
4. Review server logs

---

**API Version**: 1.0.0  
**Last Updated**: February 2026
