"""
Script sinh file âm thanh ambient và nhạc nền bản 1.4:
- rooster_morning.wav: Tiếng gà gáy sớm
- cicada_noon.wav: Tiếng ve kêu trưa hè
- cricket_night.wav: Tiếng dế mèn đêm thanh
- sea_waves.wav: Tiếng sóng biển rì rào
- bgm_chillhop_vietnam.wav: BGM phong cách Lo-fi chillhop kết hợp đàn bầu, sáo trúc, đàn tranh
"""
import os
import wave
import math
import struct
import random

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)
SAMPLE_RATE = 22050

def write_wav(filename, samples):
    filepath = os.path.join(AUDIO_DIR, filename)
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)      # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        packed = bytearray()
        for s in samples:
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767.0)
            packed.extend(struct.pack("<h", int_val))
        wav_file.writeframes(packed)
    print(f"Created: {filename}")

def gen_rooster():
    # Tiếng gà trống gáy Ò-ó-o-o (2.2s)
    duration = 2.2
    n_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * n_samples
    
    # 4 âm tiết: Ò - ó - o - oooo
    segments = [
        (0.0, 0.35, 340.0, 390.0),
        (0.4, 0.8,  520.0, 680.0),
        (0.85, 1.25, 620.0, 560.0),
        (1.3, 2.1,  480.0, 360.0)
    ]
    for start_t, end_t, f_start, f_end in segments:
        s_idx = int(start_t * SAMPLE_RATE)
        e_idx = int(end_t * SAMPLE_RATE)
        seg_len = e_idx - s_idx
        for i in range(seg_len):
            idx = s_idx + i
            if idx >= n_samples: break
            t = i / SAMPLE_RATE
            progress = i / float(seg_len)
            f = f_start + (f_end - f_start) * progress
            env = math.sin(math.pi * progress) ** 1.5
            # Tiếng gáy có độ rè kèn (harmonics)
            s = (math.sin(2.0 * math.pi * f * t) * 0.5 + 
                 math.sin(4.0 * math.pi * f * t) * 0.3 + 
                 math.sin(6.0 * math.pi * f * t) * 0.15) * env * 0.35
            samples[idx] += s
    write_wav("rooster_morning.wav", samples)

def gen_cicada():
    # Tiếng ve sầu râm ran trưa hè (rè rào dao động tầng số cao 4.0s)
    duration = 4.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Dao động rung 12 Hz
        mod = (math.sin(2.0 * math.pi * 12.0 * t) + 1.0) * 0.5
        noise = (random.random() * 2.0 - 1.0) * 0.15
        tone = math.sin(2.0 * math.pi * 4200.0 * t) * 0.35
        tone2 = math.sin(2.0 * math.pi * 4600.0 * t) * 0.2
        s = (tone + tone2 + noise) * mod * 0.28
        samples.append(s)
    write_wav("cicada_noon.wav", samples)

def gen_cricket():
    # Tiếng dế mèn gáy chi chi râm ran đêm thanh (3.5s)
    duration = 3.5
    n_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * n_samples
    
    # Chuỗi nhịp dế gáy
    for chirps in range(4):
        c_start = chirps * 0.85
        for pulse in range(3):
            p_start = c_start + pulse * 0.07
            p_len = int(0.045 * SAMPLE_RATE)
            s_idx = int(p_start * SAMPLE_RATE)
            for i in range(p_len):
                idx = s_idx + i
                if idx >= n_samples: break
                t = i / SAMPLE_RATE
                env = math.sin(math.pi * (i / float(p_len)))
                s = math.sin(2.0 * math.pi * 4800.0 * t) * env * 0.28
                samples[idx] += s
    write_wav("cricket_night.wav", samples)

def gen_sea_waves():
    # Tiếng sóng biển dạt dào êm đềm (5.0s)
    duration = 5.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Nhịp sóng dâng trào và rút
        wave_env = (math.sin(2.0 * math.pi * 0.2 * t) + 1.0) * 0.5
        # Tiếng xì xào của bọt sóng biển (pink-ish noise)
        noise = (random.random() * 2.0 - 1.0)
        s = noise * wave_env * 0.22
        samples.append(s)
    write_wav("sea_waves.wav", samples)

def gen_chillhop_bgm():
    # Nhạc nền Lofi Chillhop mộc mạc âm hưởng Đàn Tranh, Sáo Trúc, Đàn Bầu (12.0s loop)
    duration = 12.0
    n_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * n_samples
    
    # 1. Giai điệu ngũ cung Việt Nam (Hò Xự Xang Xê Cống: C D F G A C D)
    # Tần số ấm áp mang âm hưởng sáo trúc & đàn tranh
    pentatonic_notes = [
        (0.0, 523.25, 0.8),   # C5
        (0.8, 587.33, 0.8),   # D5
        (1.6, 698.46, 1.2),   # F5
        (2.8, 783.99, 0.8),   # G5
        (3.6, 880.00, 1.2),   # A5
        (4.8, 698.46, 0.8),   # F5
        (5.6, 587.33, 1.0),   # D5
        (6.8, 523.25, 1.4),   # C5
        (8.2, 440.00, 0.8),   # A4
        (9.0, 523.25, 1.0),   # C5
        (10.2, 587.33, 1.4)   # D5
    ]
    
    # 2. Hợp âm rải mộc mạc (Đàn tranh rải - Plucked harp)
    for start_t, freq, dur in pentatonic_notes:
        s_idx = int(start_t * SAMPLE_RATE)
        dur_samples = int(dur * SAMPLE_RATE)
        for i in range(dur_samples):
            idx = s_idx + i
            if idx >= n_samples: break
            t = i / SAMPLE_RATE
            # Âm sắc gảy dây đàn tranh: Decay nhanh lúc đầu, ngân đều
            pluck_env = math.exp(-t * 2.8) * 0.16
            # Cung đàn bầu luyến láy nhẹ (vibrato 5Hz)
            vibrato = math.sin(2.0 * math.pi * 5.0 * t) * 4.0
            s = (math.sin(2.0 * math.pi * (freq + vibrato) * t) * 0.65 +
                 math.sin(4.0 * math.pi * (freq + vibrato) * t) * 0.25 +
                 math.sin(6.0 * math.pi * (freq + vibrato) * t) * 0.10) * pluck_env
            samples[idx] += s
            
    # 3. Bass mộc ấm cúng (Lofi sub bass)
    bass_notes = [
        (0.0, 130.81, 2.8),  # C3
        (3.0, 174.61, 2.8),  # F3
        (6.0, 196.00, 2.8),  # G3
        (9.0, 146.83, 2.8)   # D3
    ]
    for start_t, freq, dur in bass_notes:
        s_idx = int(start_t * SAMPLE_RATE)
        dur_samples = int(dur * SAMPLE_RATE)
        for i in range(dur_samples):
            idx = s_idx + i
            if idx >= n_samples: break
            t = i / SAMPLE_RATE
            env = math.exp(-t * 0.8) * 0.10
            s = math.sin(2.0 * math.pi * freq * t) * env
            samples[idx] += s
            
    # 4. Tiếng gõ nhịp Lofi mộc (Soft rimclick & shaker)
    for step in range(24):
        click_t = step * 0.5
        s_idx = int(click_t * SAMPLE_RATE)
        for i in range(int(0.03 * SAMPLE_RATE)):
            idx = s_idx + i
            if idx >= n_samples: break
            noise = (random.random() * 2.0 - 1.0) * math.exp(-i / 150.0) * 0.04
            samples[idx] += noise

    write_wav("bgm_chillhop_vietnam.wav", samples)

if __name__ == "__main__":
    gen_rooster()
    gen_cicada()
    gen_cricket()
    gen_sea_waves()
    gen_chillhop_bgm()
    print("All 1.4 ambient & audio generated successfully!")
