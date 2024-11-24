#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile

def generate_click(duration_ms=10, samplerate=44100):
    """Generate a simple click (all ones)"""
    num_samples = int(samplerate * duration_ms / 1000)
    return np.ones(num_samples)

def generate_silence(duration_ms=250, samplerate=44100):
    """Generate silence"""
    num_samples = int(samplerate * duration_ms / 1000)
    return np.zeros(num_samples)

def main():
    # Settings
    samplerate = 44100
    
    # Generate click and silence
    click = generate_click(duration_ms=10, samplerate=samplerate)
    silence = generate_silence(duration_ms=250, samplerate=samplerate)
    
    # Convert to 16-bit integers (-32768 to 32767)
    click = np.int16(click * 32767)  # Max positive value for safe playback
    silence = np.int16(silence * 32767)
    
    # Save files
    wavfile.write('util/click.wav', samplerate, click)
    wavfile.write('util/silence.wav', samplerate, silence)
    
    print(f"Generated:")
    print(f"  click.wav: {len(click)/samplerate*1000:.1f}ms")
    print(f"  silence.wav: {len(silence)/samplerate*1000:.1f}ms")

if __name__ == '__main__':
    main()
