import torch
import numpy as np
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
import librosa

class EmotionDetector:
    def __init__(self):
        """Initialize emotion detection model"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Use a pretrained speech emotion recognition model
        # ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition is a popular choice
        model_name = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
        
        try:
            self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
            self.model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            
            # Emotion labels (from the model)
            self.emotions = ['angry', 'calm', 'disgust', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
            
        except Exception as e:
            print(f"Warning: Could not load pretrained model: {e}")
            print("Using rule-based fallback model")
            self.model = None
            self.feature_extractor = None
            self.emotions = ['neutral', 'happy', 'sad', 'angry', 'fearful', 'surprised']
    
    def predict_emotion(self, audio_data, sample_rate):
        """
        Predict emotion from audio data
        
        Args:
            audio_data: Audio samples (numpy array)
            sample_rate: Sample rate of audio
            
        Returns:
            Dictionary with emotion, confidence, and all scores
        """
        if self.model is not None:
            return self._predict_with_model(audio_data, sample_rate)
        else:
            return self._predict_with_features(audio_data, sample_rate)
    
    def _predict_with_model(self, audio_data, sample_rate):
        """Predict using pretrained transformer model"""
        try:
            # Resample to 16kHz if needed (model expects 16kHz)
            if sample_rate != 16000:
                audio_data = librosa.resample(
                    audio_data,
                    orig_sr=sample_rate,
                    target_sr=16000
                )
                sample_rate = 16000
            
            # Extract features
            inputs = self.feature_extractor(
                audio_data,
                sampling_rate=sample_rate,
                return_tensors="pt",
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Predict
            with torch.no_grad():
                logits = self.model(**inputs).logits
            
            # Get probabilities
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            probabilities = probabilities.cpu().numpy()[0]
            
            # Get predicted emotion
            predicted_idx = np.argmax(probabilities)
            predicted_emotion = self.emotions[predicted_idx]
            confidence = float(probabilities[predicted_idx])
            
            # Create scores dictionary
            scores = {emotion: float(prob) for emotion, prob in zip(self.emotions, probabilities)}
            
            return {
                'emotion': predicted_emotion,
                'confidence': round(confidence, 4),
                'scores': scores
            }
        
        except Exception as e:
            print(f"Model prediction failed: {e}, using fallback")
            return self._predict_with_features(audio_data, sample_rate)
    
    def _predict_with_features(self, audio_data, sample_rate):
        """
        Fallback: Rule-based emotion detection using audio features
        This is used when the pretrained model is not available
        """
        # Extract audio features
        features = self._extract_features(audio_data, sample_rate)
        
        # Simple rule-based classification
        energy = features['energy']
        zcr = features['zero_crossing_rate']
        pitch_mean = features['pitch_mean']
        pitch_std = features['pitch_std']
        
        # Initialize scores
        scores = {emotion: 0.0 for emotion in self.emotions}
        
        # Rule-based scoring
        # High energy + high pitch variation = angry or surprised
        if energy > 0.5:
            if pitch_std > 50:
                scores['angry'] = 0.4
                scores['surprised'] = 0.3
            else:
                scores['happy'] = 0.5
        # Low energy = sad or calm
        elif energy < 0.2:
            if pitch_mean < 150:
                scores['sad'] = 0.6
            else:
                scores['neutral'] = 0.5
        # Medium energy
        else:
            if zcr > 0.1:
                scores['fearful'] = 0.4
            scores['neutral'] = 0.4
        
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: v/total for k, v in scores.items()}
        else:
            scores['neutral'] = 1.0
        
        # Get predicted emotion
        predicted_emotion = max(scores.items(), key=lambda x: x[1])[0]
        confidence = scores[predicted_emotion]
        
        return {
            'emotion': predicted_emotion,
            'confidence': round(confidence, 4),
            'scores': scores
        }
    
    def _extract_features(self, audio_data, sample_rate):
        """Extract audio features for rule-based classification"""
        # Energy
        energy = np.sum(audio_data ** 2) / len(audio_data)
        
        # Zero crossing rate
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data))
        
        # Pitch (F0)
        try:
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sample_rate)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            pitch_mean = np.mean(pitch_values) if pitch_values else 0
            pitch_std = np.std(pitch_values) if pitch_values else 0
        except:
            pitch_mean = 0
            pitch_std = 0
        
        return {
            'energy': energy,
            'zero_crossing_rate': zcr,
            'pitch_mean': pitch_mean,
            'pitch_std': pitch_std
        }
