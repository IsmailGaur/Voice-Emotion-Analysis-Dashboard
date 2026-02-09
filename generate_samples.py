#!/usr/bin/env python
"""
Generate sample audio files for testing the Voice Emotion Analysis system

This script creates synthetic audio with varying characteristics
that can be used to test the emotion detection system.
"""

import numpy as np
import soundfile as sf
import os

def generate_tone(frequency, duration, sample_rate=16000, amplitude=0.3):
    """Generate a simple sine wave tone"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def generate_emotional_audio(emotion, duration=5, sample_rate=16000):
    """
    Generate synthetic audio that mimics emotional characteristics
    
    Args:
        emotion: One of ['happy', 'sad', 'angry', 'neutral', 'fearful']
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
    
    Returns:
        numpy array of audio samples
    """
    
    # Different emotions have different acoustic characteristics
    if emotion == 'happy':
        # Higher pitch, more variation
        base_freq = 300
        freq_variation = 50
        energy = 0.4
        
    elif emotion == 'sad':
        # Lower pitch, less variation
        base_freq = 150
        freq_variation = 10
        energy = 0.2
        
    elif emotion == 'angry':
        # High pitch, high energy, sharp transitions
        base_freq = 350
        freq_variation = 80
        energy = 0.5
        
    elif emotion == 'fearful':
        # Unstable pitch, medium-high energy
        base_freq = 280
        freq_variation = 100
        energy = 0.35
        
    else:  # neutral
        # Moderate everything
        base_freq = 200
        freq_variation = 20
        energy = 0.3
    
    # Generate audio with varying pitch
    audio = np.array([])
    chunk_duration = 0.1  # 100ms chunks
    num_chunks = int(duration / chunk_duration)
    
    for i in range(num_chunks):
        # Vary frequency
        freq = base_freq + np.random.uniform(-freq_variation, freq_variation)
        chunk = generate_tone(freq, chunk_duration, sample_rate, energy)
        
        # Add some noise for realism
        noise = np.random.normal(0, 0.01, len(chunk))
        chunk = chunk + noise
        
        audio = np.concatenate([audio, chunk])
    
    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.9
    
    return audio.astype(np.float32)

def generate_mixed_emotion_audio(emotions, durations, sample_rate=16000):
    """
    Generate audio with multiple emotions in sequence
    
    Args:
        emotions: List of emotion names
        durations: List of durations for each emotion
        sample_rate: Sample rate
    
    Returns:
        numpy array of audio samples
    """
    audio_segments = []
    
    for emotion, duration in zip(emotions, durations):
        segment = generate_emotional_audio(emotion, duration, sample_rate)
        audio_segments.append(segment)
    
    return np.concatenate(audio_segments)

def main():
    """Generate sample audio files"""
    
    output_dir = 'sample_audio'
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating sample audio files...")
    print("=" * 60)
    
    # Generate single-emotion samples
    emotions = ['happy', 'sad', 'angry', 'neutral', 'fearful']
    
    for emotion in emotions:
        filename = f"{output_dir}/sample_{emotion}.wav"
        audio = generate_emotional_audio(emotion, duration=10)
        sf.write(filename, audio, 16000)
        print(f"✓ Generated: {filename}")
    
    # Generate mixed-emotion sample
    mixed_emotions = ['neutral', 'happy', 'angry', 'sad', 'fearful', 'happy']
    mixed_durations = [3, 3, 3, 3, 3, 3]  # 18 seconds total
    
    mixed_audio = generate_mixed_emotion_audio(mixed_emotions, mixed_durations)
    mixed_filename = f"{output_dir}/sample_mixed_emotions.wav"
    sf.write(mixed_filename, mixed_audio, 16000)
    print(f"✓ Generated: {mixed_filename}")
    print(f"  Sequence: {' → '.join(mixed_emotions)}")
    
    # Generate conversation-like sample
    conversation = ['neutral', 'happy', 'happy', 'angry', 'angry', 'sad', 'neutral']
    conv_durations = [2, 2, 2, 2, 2, 2, 2]  # 14 seconds
    
    conv_audio = generate_mixed_emotion_audio(conversation, conv_durations)
    conv_filename = f"{output_dir}/sample_conversation.wav"
    sf.write(conv_filename, conv_audio, 16000)
    print(f"✓ Generated: {conv_filename}")
    print(f"  Sequence: {' → '.join(conversation)}")
    
    print("=" * 60)
    print(f"\n✓ All sample files created in '{output_dir}/' directory")
    print("\nYou can now test the application with these files:")
    print("  1. Start the app: python app.py")
    print("  2. Upload any sample file from the sample_audio/ directory")
    print("  3. Click 'Analyze Audio' to see emotion detection results")
    print("\nNote: These are synthetic samples. Real voice recordings")
    print("will produce more accurate emotion detection results.")

if __name__ == "__main__":
    main()
