import tkinter as tk
from tkinter import filedialog
import threading
import pyaudio
import wave
from pydub import AudioSegment
import io
import os

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Standard voice rate

# Global variables
p = pyaudio.PyAudio()
real_mic = None
virtual_mic = None
sound_to_play = None
sound_position = 0
is_running = True

def init_audio():
    global real_mic, virtual_mic
    # Find default devices
    input_index = p.get_default_input_device_info()['index']
    output_index = p.get_default_output_device_info()['index']
    
    real_mic = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                     input=True, input_device_index=input_index, frames_per_buffer=CHUNK)
    virtual_mic = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                        output=True, output_device_index=output_index, frames_per_buffer=CHUNK)

def play_sound(sound_file):
    global sound_to_play, sound_position
    try:
        # Load any audio format
        audio = AudioSegment.from_file(sound_file)
        # Convert to standard format
        audio = audio.set_frame_rate(RATE).set_channels(CHANNELS).set_sample_width(2)
        # Get raw data
        raw_data = audio.raw_data
        sound_to_play = raw_data
        sound_position = 0
        print(f"Playing: {os.path.basename(sound_file)}")
    except Exception as e:
        print(f"Error loading sound: {e}")

def audio_loop():
    global sound_to_play, sound_position, is_running
    init_audio()
    
    while is_running:
        try:
            # Get user's voice
            voice_data = real_mic.read(CHUNK, exception_on_overflow=False)
            output_data = voice_data  # Default to voice
            
            # Inject sound if playing
            if sound_to_play and sound_position < len(sound_to_play):
                chunk_end = sound_position + CHUNK * 2  # 16-bit = 2 bytes per sample
                sound_chunk = sound_to_play[sound_position:chunk_end]
                sound_position = chunk_end
                
                # Pad if sound chunk is smaller
                if len(sound_chunk) < len(voice_data):
                    sound_chunk += b'\x00' * (len(voice_data) - len(sound_chunk))
                
                output_data = sound_chunk
                
                # Clear sound when done
                if sound_position >= len(sound_to_play):
                    sound_to_play = None
                    sound_position = 0
            
            # Send to output
            virtual_mic.write(output_data)
        except Exception as e:
            print(f"Audio error: {e}")
            break

# UI
root = tk.Tk()
root.title("AuraBoard")
root.geometry("300x400")

sounds = {}

def add_sound():
    filepath = filedialog.askopenfilename(
        filetypes=[("Audio", "*.mp3 *.wav *.ogg *.m4a *.flac *.aiff")]
    )
    if filepath:
        name = os.path.basename(filepath)
        sounds[name] = filepath
        btn = tk.Button(sound_frame, text=name, command=lambda f=filepath: play_sound(f))
        btn.pack(fill='x', pady=2)

def on_closing():
    global is_running
    is_running = False
    root.destroy()

# UI Layout
tk.Label(root, text="AuraBoard", font=('Arial', 14)).pack(pady=10)
tk.Button(root, text="+ Add Sound", command=add_sound).pack(pady=5)

sound_frame = tk.Frame(root)
sound_frame.pack(fill='both', expand=True, padx=10)

# Start audio thread
audio_thread = threading.Thread(target=audio_loop, daemon=True)
audio_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# Cleanup
is_running = False
if real_mic: real_mic.stop_stream()
if virtual_mic: virtual_mic.stop_stream()
p.terminate()