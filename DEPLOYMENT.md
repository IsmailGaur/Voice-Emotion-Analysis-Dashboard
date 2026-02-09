# 🚀 Deployment Guide

This guide will help you deploy the Voice Emotion Analysis application to production.

## Table of Contents

1. [Render Deployment](#render-deployment)
2. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
3. [Vercel Deployment](#vercel-deployment)
4. [Environment Variables](#environment-variables)
5. [Troubleshooting](#troubleshooting)

---

## 1. Render Deployment (Recommended)

Render is the easiest platform to deploy this application.

### Step-by-Step Guide

#### 1.1 Prepare Your Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Create a GitHub repository and push
git remote add origin https://github.com/yourusername/voice-emotion-app.git
git branch -M main
git push -u origin main
```

#### 1.2 Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Connect your GitHub account

#### 1.3 Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure settings:
   - **Name**: `voice-emotion-app` (or your choice)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

#### 1.4 Advanced Settings

Add environment variables (optional):
```
PYTHON_VERSION=3.11.0
```

Configure disk storage:
- **Name**: `uploads`
- **Mount Path**: `/opt/render/project/src/uploads`
- **Size**: 1 GB (free tier)

#### 1.5 Deploy

1. Click "Create Web Service"
2. Wait for build and deployment (5-10 minutes)
3. Your app will be live at: `https://voice-emotion-app.onrender.com`

### Render Configuration Files

The repository includes:
- `Procfile`: Defines the start command
- `render.yaml`: Service configuration

### Free Tier Limitations

- App spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month free (sufficient for most use cases)

---

## 2. Streamlit Cloud Deployment

For a simpler Streamlit version:

### 2.1 Create Streamlit App

Create `streamlit_app.py`:

```python
import streamlit as st
from audio_processing.preprocess import AudioProcessor
from emotion_model.model import EmotionDetector
import plotly.graph_objects as go

st.set_page_config(page_title="Voice Emotion Analysis", page_icon="🎤")

st.title("🎤 Voice Emotion Analysis")

uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3', 'flac'])

if uploaded_file:
    with st.spinner("Analyzing..."):
        # Process and analyze
        processor = AudioProcessor()
        detector = EmotionDetector()
        
        # Save and process file
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        chunks = processor.process_audio("temp_audio.wav")
        results = []
        
        for chunk in chunks:
            emotion_data = detector.predict_emotion(
                chunk['audio_data'],
                chunk['sample_rate']
            )
            results.append({
                'start_time': chunk['start_time'],
                'end_time': chunk['end_time'],
                'emotion': emotion_data['emotion'],
                'confidence': emotion_data['confidence']
            })
        
        # Display results
        st.success("Analysis complete!")
        
        # Show charts using Plotly
        # ... (add visualization code)
```

### 2.2 Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select repository and branch
5. Set main file to `streamlit_app.py`
6. Deploy

---

## 3. Vercel Deployment (Backend + Frontend Split)

### 3.1 Backend on Render

Deploy the Flask API on Render (see Section 1)

### 3.2 Frontend on Vercel

Create a static frontend:

```bash
mkdir frontend
cd frontend
# Create static HTML/CSS/JS files
```

Deploy to Vercel:

```bash
npm install -g vercel
vercel login
vercel
```

Update API endpoint in frontend to point to Render backend.

---

## 4. Environment Variables

### Required Variables

None for basic functionality.

### Optional Variables

```bash
# Model caching
HF_HOME=/path/to/cache

# Flask configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key

# Gunicorn settings
WORKERS=2
THREADS=4
TIMEOUT=120
```

---

## 5. Troubleshooting

### Build Failures

**Issue**: Dependencies fail to install

**Solution**:
```bash
# Update requirements.txt with specific versions
pip freeze > requirements.txt

# Or use lighter dependencies
torch==2.1.0+cpu  # CPU-only PyTorch
```

### Memory Issues

**Issue**: App crashes due to memory limits

**Solution**:
1. Upgrade to Render's paid plan (more RAM)
2. Reduce chunk duration to use less memory
3. Use lighter models

### Model Download Fails

**Issue**: Transformer model won't download

**Solution**:
1. Pre-download and include in repository
2. Use fallback rule-based model
3. Set `HF_HOME` environment variable

### Slow Cold Starts

**Issue**: First request takes too long

**Solution**:
1. Upgrade to paid Render plan (no spin-down)
2. Implement model caching
3. Use smaller models

### File Upload Issues

**Issue**: Large files fail to upload

**Solution**:
```python
# In app.py, adjust max file size
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Port Configuration

**Issue**: App not accessible

**Solution**:
```python
# Ensure app.py uses environment PORT
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

---

## 6. Monitoring & Logs

### Render Logs

View logs in Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. Monitor real-time logs

### Error Tracking

Add error logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In your routes
try:
    # ... code
except Exception as e:
    logger.error(f"Error: {str(e)}")
```

---

## 7. Performance Optimization

### Caching Models

```python
# Cache model downloads
import os
os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
```

### Gunicorn Workers

```python
# Procfile
web: gunicorn app:app --workers=2 --threads=4 --timeout=120
```

### Request Timeout

```python
# For long audio files
--timeout=300  # 5 minutes
```

---

## 8. Security

### HTTPS

Render provides HTTPS automatically.

### API Rate Limiting

Add Flask-Limiter:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_audio():
    # ...
```

### File Validation

Already implemented in `app.py`:
- File type checking
- File size limits
- Secure filename handling

---

## 9. Backup & Recovery

### Database (if added later)

Use Render's managed PostgreSQL for data persistence.

### Model Files

Store model files in:
1. Git LFS for version control
2. Cloud storage (S3, GCS) for production
3. Render disk storage for caching

---

## 10. Cost Estimation

### Free Tier (Render)

- **Cost**: $0/month
- **Limitations**: 
  - 750 hours/month
  - Spins down after inactivity
  - 512 MB RAM

### Paid Tier (Render)

- **Starter**: $7/month
  - Always on
  - 512 MB RAM
  
- **Standard**: $25/month
  - Always on
  - 2 GB RAM
  - Faster builds

---

## 11. Checklist

Before deploying:

- [ ] All tests pass (`python test_setup.py`)
- [ ] Dependencies listed in `requirements.txt`
- [ ] Procfile configured
- [ ] Environment variables set
- [ ] Git repository created
- [ ] .gitignore configured
- [ ] README.md complete
- [ ] License file added

After deployment:

- [ ] Test all features on live URL
- [ ] Check upload functionality
- [ ] Verify emotion detection works
- [ ] Test export features
- [ ] Monitor logs for errors
- [ ] Set up error alerts

---

## 12. Support

For deployment issues:

1. Check Render documentation: [render.com/docs](https://render.com/docs)
2. Review application logs
3. Verify all files are committed to git
4. Test locally before deploying

---

**Happy Deploying! 🚀**
