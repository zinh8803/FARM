import os
import wave
import math
import struct

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

SAMPLE_RATE = 22050

def write_wav(filename, samples):
    filepath = os.path.join(AUDIO_DIR, filename)
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)      # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        # Convert float -1.0..1.0 to int16
        packed = bytearray()
        for s in samples:
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767.0)
            packed.extend(struct.pack("<h", int_val))
        wav_file.writeframes(packed)
    print(f"Created: {filepath} ({len(samples)} samples)")

def gen_click():
    # Crisp, soft wooden click sound for UI buttons
    duration = 0.05
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    freq = 600.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 60.0)
        s = math.sin(2.0 * math.pi * freq * t) * env * 0.4
        samples.append(s)
    write_wav("click.wav", samples)

def gen_toggle():
    # Pleasant two-tone chime toggle
    duration = 0.08
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 440.0 if t < 0.04 else 660.0
        env = math.exp(-(t % 0.04) * 50.0)
        s = math.sin(2.0 * math.pi * freq * t) * env * 0.35
        samples.append(s)
    write_wav("toggle.wav", samples)

def gen_tool():
    # Soft thud / hoe soil swing
    duration = 0.1
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 180.0 * (1.0 - t / duration) + 60.0
        env = (1.0 - t / duration) ** 2
        noise = (math.sin(i * 123.456) % 1.0) * 0.2
        s = (math.sin(2.0 * math.pi * freq * t) * 0.5 + noise) * env * 0.5
        samples.append(s)
    write_wav("tool.wav", samples)

def gen_water():
    # Pleasant droplet / water splash sound
    duration = 0.12
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 500.0 + 300.0 * math.sin(t * 80.0)
        env = math.exp(-t * 25.0)
        s = math.sin(2.0 * math.pi * freq * t) * env * 0.4
        samples.append(s)
    write_wav("water.wav", samples)

def gen_plant():
    # Little upbeat chirp when planting seeds
    duration = 0.1
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 523.25 + (783.99 - 523.25) * (t / duration)
        env = math.sin(math.pi * (t / duration))
        s = math.sin(2.0 * math.pi * freq * t) * env * 0.35
        samples.append(s)
    write_wav("plant.wav", samples)

def gen_harvest():
    # Victorious pleasant chime chord (Arpeggio: C - E - G - C)
    duration = 0.28
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    notes = [523.25, 659.25, 783.99, 1046.50]
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        note_idx = min(int(t / (duration / 4.0)), 3)
        freq = notes[note_idx]
        note_t = t - note_idx * (duration / 4.0)
        env = math.exp(-note_t * 18.0)
        s = math.sin(2.0 * math.pi * freq * t) * env * 0.35
        samples.append(s)
    write_wav("harvest.wav", samples)

def gen_bgm():
    # Peaceful acoustic retro ambient melody loop (4 measures, 8 seconds)
    # Pentatonic relaxing rural Vietnamese / country farm scale (C - D - E - G - A)
    duration = 8.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * n_samples
    
    # Melody notes: (start_time, note_freq, note_duration)
    # C4=261.63, D4=293.66, E4=329.63, G4=392.00, A4=440.00, C5=523.25, D5=587.33, E5=659.25
    melody = [
        (0.0, 329.63, 0.6),   # E4
        (0.8, 392.00, 0.6),   # G4
        (1.6, 440.00, 0.8),   # A4
        (2.4, 523.25, 0.6),   # C5
        (3.2, 440.00, 0.6),   # A4
        (4.0, 392.00, 0.8),   # G4
        (4.8, 329.63, 0.6),   # E4
        (5.6, 293.66, 0.8),   # D4
        (6.4, 261.63, 1.2),   # C4
    ]
    
    # Bass notes
    bass = [
        (0.0, 130.81, 1.8),   # C3
        (2.0, 164.81, 1.8),   # E3
        (4.0, 196.00, 1.8),   # G3
        (6.0, 130.81, 1.8),   # C3
    ]
    
    for start_t, freq, dur in melody:
        start_idx = int(start_t * SAMPLE_RATE)
        dur_samples = int(dur * SAMPLE_RATE)
        for i in range(dur_samples):
            idx = start_idx + i
            if idx >= n_samples:
                break
            t = i / SAMPLE_RATE
            env = math.sin(math.pi * (i / dur_samples)) * math.exp(-t * 2.0)
            # Add fundamental + warm harmonic
            s = (math.sin(2.0 * math.pi * freq * t) * 0.7 + 
                 math.sin(4.0 * math.pi * freq * t) * 0.25 +
                 math.sin(6.0 * math.pi * freq * t) * 0.05) * env * 0.14
            samples[idx] += s
            
    for start_t, freq, dur in bass:
        start_idx = int(start_t * SAMPLE_RATE)
        dur_samples = int(dur * SAMPLE_RATE)
        for i in range(dur_samples):
            idx = start_idx + i
            if idx >= n_samples:
                break
            t = i / SAMPLE_RATE
            env = math.exp(-t * 1.5)
            s = math.sin(2.0 * math.pi * freq * t) * env * 0.10
            samples[idx] += s
            
    write_wav("bgm_farm.wav", samples)

if __name__ == "__main__":
    gen_click()
    gen_toggle()
    gen_tool()
    gen_water()
    gen_plant()
    gen_harvest()
    gen_bgm()
    print("All audio generated successfully!")
