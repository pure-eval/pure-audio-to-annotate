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
   
   # Generate base components
   click = generate_click(duration_ms=10, samplerate=samplerate)
   silence = generate_silence(duration_ms=250, samplerate=samplerate)
   
   # Convert to 16-bit integers (-32768 to 32767)
   click_int = np.int16(click * 32767)
   silence_int = np.int16(silence * 32767)
   
   # Create and convert combined segments 
   click_silence = np.int16(np.concatenate([click, silence]) * 32767)
   silence_click_silence = np.int16(np.concatenate([silence, click, silence]) * 32767)
   
   # Save all files
   wavfile.write('util/click.wav', samplerate, click_int)
   wavfile.write('util/silence.wav', samplerate, silence_int)
   wavfile.write('util/click_silence.wav', samplerate, click_silence)
   wavfile.write('util/silence_click_silence.wav', samplerate, silence_click_silence)
   
   print(f"Generated:")
   print(f"  click.wav: {len(click_int)/samplerate*1000:.1f}ms")
   print(f"  silence.wav: {len(silence_int)/samplerate*1000:.1f}ms")
   print(f"  click_silence.wav: {len(click_silence)/samplerate*1000:.1f}ms")
   print(f"  silence_click_silence.wav: {len(silence_click_silence)/samplerate*1000:.1f}ms")

if __name__ == '__main__':
   main()