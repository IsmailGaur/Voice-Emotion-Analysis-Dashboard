# 🚀 Quick Start Guide

Get the Voice Emotion Analysis app running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- pip package manager
- 2GB free disk space (for model downloads)

## Installation Steps

### 1. Clone or Download

```bash
# If you have git
git clone <repository-url>
cd voice-emotion-app

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 2-5 minutes depending on your internet speed.

### 4. Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 5. Open in Browser

Navigate to: `http://localhost:5000`

## First-Time Use

### Test with Sample Audio

1. Generate sample audio files:
```bash
python generate_samples.py
```

2. In the browser:
   - Click "Choose File"
   - Select `sample_audio/sample_mixed_emotions.wav`
   - Click "Analyze Audio"
   - Wait 5-10 seconds
   - View results!

### Upload Your Own Audio

Supported formats: **WAV, MP3, FLAC, OGG, M4A**

1. Click "Choose File" or drag & drop
2. Click "Analyze Audio"
3. View the emotion timeline and charts

## Understanding Results

### Summary Cards
- **Dominant Emotion**: Most frequent emotion detected
- **Total Duration**: Length of your audio file
- **Emotion Changes**: Number of emotion transitions

### Emotion Timeline
Shows how emotions change over time with timestamps

### Charts
- **Timeline Chart**: Emotions plotted over time
- **Pie Chart**: Percentage distribution of emotions
- **Bar Chart**: Frequency of each emotion

### Detailed Table
Chunk-by-chunk breakdown with:
- Start/End times
- Detected emotion
- Confidence score

## Export Results

Click the export buttons to download:
- **CSV**: For spreadsheet analysis
- **JSON**: For further processing

## Common Issues

### Issue: Dependencies fail to install

**Solution**:
```bash
# Install system dependencies first (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev portaudio19-dev ffmpeg

# macOS
brew install python@3.11 portaudio ffmpeg

# Then retry pip install
pip install -r requirements.txt
```

### Issue: Model download is slow

**Solution**: First run downloads ~1.2GB model. Be patient!

```bash
# Check progress
# Model downloads to ~/.cache/huggingface/
```

### Issue: Out of memory error

**Solution**: Reduce chunk duration in code:
```python
# In app.py, change:
audio_processor = AudioProcessor(chunk_duration=2.0)  # Smaller chunks
```

### Issue: Port 5000 already in use

**Solution**: Use a different port:
```bash
# In app.py, change the port:
app.run(port=8000)
```

## Tips for Best Results

1. **Audio Quality**:
   - Use clear recordings
   - Minimize background noise
   - Single speaker works best

2. **File Size**:
   - Keep files under 50MB
   - Longer files take more time to process

3. **Emotion Detection**:
   - First run may be slower (model loading)
   - Subsequent analyses are faster
   - Confidence > 70% indicates reliable detection

## What's Next?

### Customize Settings

Edit configuration in source files:
- Chunk duration: `audio_processing/preprocess.py`
- Model selection: `emotion_model/model.py`
- UI styling: `static/css/style.css`

### Deploy to Production

See `DEPLOYMENT.md` for complete deployment guide to:
- Render (recommended)
- Streamlit Cloud
- Vercel

### Add Features

Ideas for enhancement:
- Real-time microphone input
- Multiple speaker detection
- Emotion intensity levels
- Custom emotion categories

## Need Help?

1. Check `README.md` for detailed documentation
2. Run tests: `python test_setup.py`
3. Review error logs in terminal
4. Check GitHub issues

## Performance Benchmarks

| Audio Length | Processing Time | Model Size |
|--------------|----------------|------------|
| 10 seconds   | ~3-5 seconds   | 1.2 GB     |
| 30 seconds   | ~10-15 seconds | 1.2 GB     |
| 1 minute     | ~20-30 seconds | 1.2 GB     |
| 5 minutes    | ~2-3 minutes   | 1.2 GB     |

*Times on average laptop with CPU processing*

## Keyboard Shortcuts

- **Drag & Drop**: Upload file
- **Enter**: Analyze (when file selected)
- **Esc**: Clear results

---

**You're all set! 🎉**

Start analyzing emotions in voice recordings!

For questions or issues, check the main README.md or open a GitHub issue.
