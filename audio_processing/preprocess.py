import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import os

class AudioProcessor:
    def __init__(self, chunk_duration=3.0, sample_rate=16000):
        """
        Initialize audio processor
        
        Args:
            chunk_duration: Duration of each chunk in seconds (default: 3 seconds)
            sample_rate: Target sample rate (default: 16000 Hz)
        """
        self.chunk_duration = chunk_duration
        self.sample_rate = sample_rate
    
    def process_audio(self, audio_path):
        """
        Process audio file and split into chunks
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            List of chunks with metadata
        """
        # Load audio file
        audio_data, original_sr = self._load_audio(audio_path)
        
        # Resample if needed
        if original_sr != self.sample_rate:
            audio_data = librosa.resample(
                audio_data,
                orig_sr=original_sr,
                target_sr=self.sample_rate
            )
        
        # Split into chunks
        chunks = self._split_into_chunks(audio_data, self.sample_rate)
        
        return chunks
    
    def _load_audio(self, audio_path):
        """Load audio file and convert to mono"""
        try:
            # Try loading with librosa first
            audio_data, sr = librosa.load(audio_path, sr=None, mono=True)
            return audio_data, sr
        except Exception as e:
            # If librosa fails, try with pydub (for mp3, etc.)
            try:
                audio = AudioSegment.from_file(audio_path)
                
                # Convert to mono
                if audio.channels > 1:
                    audio = audio.set_channels(1)
                
                # Get sample rate
                sr = audio.frame_rate
                
                # Convert to numpy array
                audio_data = np.array(audio.get_array_of_samples()).astype(np.float32)
                
                # Normalize
                audio_data = audio_data / np.max(np.abs(audio_data))
                
                return audio_data, sr
            except Exception as e2:
                raise Exception(f"Failed to load audio file: {str(e2)}")
    
    def _split_into_chunks(self, audio_data, sample_rate):
        """Split audio into fixed-duration chunks"""
        chunk_samples = int(self.chunk_duration * sample_rate)
        total_samples = len(audio_data)
        
        chunks = []
        current_position = 0
        
        while current_position < total_samples:
            # Calculate chunk boundaries
            start_sample = current_position
            end_sample = min(current_position + chunk_samples, total_samples)
            
            # Extract chunk
            chunk_audio = audio_data[start_sample:end_sample]
            
            # Pad if chunk is too short (last chunk)
            if len(chunk_audio) < chunk_samples:
                chunk_audio = np.pad(
                    chunk_audio,
                    (0, chunk_samples - len(chunk_audio)),
                    mode='constant'
                )
            
            # Calculate timestamps
            start_time = start_sample / sample_rate
            end_time = end_sample / sample_rate
            
            chunks.append({
                'audio_data': chunk_audio,
                'sample_rate': sample_rate,
                'start_time': round(start_time, 2),
                'end_time': round(end_time, 2),
                'duration': round(end_time - start_time, 2)
            })
            
            current_position = end_sample
        
        return chunks
    
    @staticmethod
    def format_timestamp(seconds):
        """Convert seconds to MM:SS format"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
