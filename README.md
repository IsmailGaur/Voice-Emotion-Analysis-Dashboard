# 🎤 Voice Emotion Analysis Dashboard

A complete AI-powered application that analyzes human voice/audio input, detects sentiment and emotions over time, and visualizes them in an interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **Audio Input**: Upload audio files (WAV, MP3, FLAC, OGG, M4A) or use drag-and-drop
- **Emotion Detection**: Real-time emotion recognition using deep learning models
- **Timestamp Tracking**: Precise emotion detection at specific timestamps (MM:SS)
- **Emotion Timeline**: Visual representation of emotions changing over time
- **Interactive Charts**: 
  - Emotion timeline graph
  - Emotion distribution pie chart
  - Emotion frequency bar chart
- **Emotion Change Detection**: Automatically detects and logs when emotions change
- **Statistics Dashboard**: Overall sentiment summary with dominant emotion analysis
- **Export Options**: Export results as CSV or JSON
- **Responsive Design**: Beautiful UI that works on desktop and mobile

## 🧠 How It Works

### Model Architecture

The application uses a **wav2vec2-based Speech Emotion Recognition (SER)** model:

- **Primary Model**: `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`
  - Pre-trained on speech emotion datasets
  - Fine-tuned for 8 emotion classes
  - Uses transformer-based architecture for superior accuracy

- **Fallback System**: Rule-based emotion detection using audio features
  - Extracts features: energy, zero-crossing rate, pitch statistics
  - Provides reliable backup when the transformer model is unavailable

### Emotion Detection Process

1. **Audio Processing**:
   - Convert audio to mono channel
   - Resample to 16kHz (standard for speech models)
   - Split into 3-second chunks for analysis

2. **Feature Extraction**:
   - wav2vec2 extracts high-level audio representations
   - Features capture prosody, tone, and acoustic patterns

3. **Emotion Classification**:
   - Neural network predicts emotion probabilities
   - Detects: Angry, Calm, Disgust, Fearful, Happy, Neutral, Sad, Surprised

4. **Temporal Analysis**:
   - Tracks emotions across time
   - Detects emotion transitions
   - Calculates confidence scores

## 📊 Detected Emotions

| Emotion | Description | Audio Characteristics |
|---------|-------------|----------------------|
| 😠 Angry | High arousal, negative valence | High energy, elevated pitch |
| 😌 Calm | Low arousal, positive valence | Low energy, stable pitch |
| 🤢 Disgust | Negative valence | Specific vocal patterns |
| 😨 Fearful | High arousal, negative valence | High pitch variability |
| 😊 Happy | High arousal, positive valence | High energy, varied pitch |
| 😐 Neutral | Baseline emotional state | Moderate energy and pitch |
| 😢 Sad | Low arousal, negative valence | Low energy, low pitch |
| 😲 Surprised | High arousal | Sudden changes in pitch |

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git

### Local Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd voice-emotion-app
```

2. **Create virtual environment**:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

5. **Access the dashboard**:
Open your browser and navigate to `http://localhost:5000`

## 🌐 Deployment

### Deploy on Render

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Select "Python" as the environment
   - Render will automatically detect `render.yaml`

3. **Configuration**:
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.11

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Access your live URL: `https://your-app-name.onrender.com`

### Deploy on Streamlit Cloud (Alternative)

For a Streamlit version, create `streamlit_app.py`:

```python
import streamlit as st
# Implement Streamlit UI
# See documentation at streamlit.io
```

Then deploy at [streamlit.io/cloud](https://streamlit.io/cloud)

### Deploy on Vercel (API + Frontend Split)

1. Deploy backend on Render
2. Deploy static frontend on Vercel
3. Configure API endpoints in frontend

## 📁 Project Structure

```
voice-emotion-app/
│
├── app.py                      # Main Flask application
├── emotion_model/
│   ├── __init__.py
│   └── model.py               # Emotion detection model
├── audio_processing/
│   ├── __init__.py
│   └── preprocess.py          # Audio preprocessing utilities
├── templates/
│   └── dashboard.html         # Main dashboard template
├── static/
│   ├── css/
│   │   └── style.css         # Stylesheet
│   └── js/
│       └── script.js         # Frontend JavaScript
├── uploads/                   # Temporary audio storage
├── requirements.txt           # Python dependencies
├── Procfile                   # Render deployment config
├── render.yaml               # Render service config
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🎯 Usage

1. **Upload Audio**:
   - Click "Choose File" or drag-and-drop your audio file
   - Supported formats: WAV, MP3, FLAC, OGG, M4A
   - Maximum file size: 50MB

2. **Analyze**:
   - Click "Analyze Audio" button
   - Wait for processing (typically 5-30 seconds)

3. **View Results**:
   - **Summary Cards**: See dominant emotion, total duration, and change count
   - **Emotion Changes**: Review exact timestamps of emotion transitions
   - **Timeline Chart**: Visualize emotions over time
   - **Distribution Charts**: Understand emotion proportions
   - **Detailed Table**: Examine chunk-by-chunk analysis

4. **Export**:
   - Download results as CSV for spreadsheet analysis
   - Download results as JSON for further processing

## 📈 Example Output

```
Emotion Timeline:
00:00 - 00:03 → Neutral (85.3%)
00:03 - 00:06 → Happy (78.9%)
00:06 - 00:09 → Happy (82.1%)
00:09 - 00:12 → Angry (91.4%)
00:12 - 00:15 → Sad (76.8%)

Emotion Changes:
00:03 → Neutral to Happy
00:09 → Happy to Angry
00:12 → Angry to Sad

Statistics:
- Dominant Emotion: Happy (40%)
- Total Duration: 15 seconds
- Emotion Distribution:
  * Happy: 40%
  * Angry: 20%
  * Neutral: 20%
  * Sad: 20%
```

## 🛠️ Technical Details

### Dependencies

- **Flask**: Web framework for API and routing
- **librosa**: Audio processing and feature extraction
- **transformers**: HuggingFace transformers for wav2vec2
- **PyTorch**: Deep learning framework
- **soundfile**: Audio file I/O
- **pydub**: Audio format conversion
- **Plotly**: Interactive data visualization
- **gunicorn**: Production WSGI server

### Performance

- **Chunk Duration**: 3 seconds (configurable)
- **Sample Rate**: 16kHz (standard for speech)
- **Processing Speed**: ~1-2 seconds per 3-second chunk
- **Model Size**: ~1.2GB (downloaded on first run)

### API Endpoints

- `GET /`: Main dashboard
- `POST /analyze`: Analyze audio file
- `GET /health`: Health check

## 🔧 Configuration

Edit `audio_processing/preprocess.py` to adjust:

```python
chunk_duration = 3.0  # Chunk size in seconds
sample_rate = 16000   # Audio sample rate
```

Edit `emotion_model/model.py` to change the model:

```python
model_name = "your-model-name"  # HuggingFace model ID
```

## 🎨 Customization

### Add New Emotions

1. Update emotion list in `emotion_model/model.py`
2. Add corresponding CSS classes in `static/css/style.css`
3. Update color mapping in `static/js/script.js`

### Change Chunk Duration

Modify `AudioProcessor` initialization in `app.py`:

```python
audio_processor = AudioProcessor(chunk_duration=5.0)  # 5-second chunks
```

### Adjust Confidence Threshold

Filter low-confidence predictions in `app.py`:

```python
if emotion_data['confidence'] < 0.7:
    # Handle low confidence
```

## 🐛 Troubleshooting

### Model Download Issues

If the transformer model fails to download:

```bash
# Set HuggingFace cache directory
export HF_HOME=/path/to/cache
```

### Audio Format Errors

Install ffmpeg for broader format support:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from ffmpeg.org
```

### Memory Issues

For large audio files, reduce chunk duration or use streaming:

```python
# Reduce chunk size
chunk_duration = 2.0  # Smaller chunks = less memory
```

## 🚧 Future Enhancements

- [ ] Real-time microphone recording
- [ ] Multi-language support
- [ ] Speaker diarization (multiple speakers)
- [ ] Emotion intensity levels
- [ ] Custom model training interface
- [ ] Audio preprocessing filters
- [ ] Batch processing multiple files
- [ ] API authentication
- [ ] Database storage for history
- [ ] Dark mode toggle

## 📄 License

MIT License - feel free to use and modify for your projects.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

## 🙏 Acknowledgments

- **HuggingFace** for transformer models
- **librosa** team for audio processing tools
- **Plotly** for visualization library
- **Flask** community for web framework

---

**Built with ❤️ using Flask, PyTorch, and Transformers**

*Last Updated: February 2026*
