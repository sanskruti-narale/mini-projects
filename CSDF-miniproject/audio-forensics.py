import os
import tkinter as tk
from tkinter import filedialog, messagebox
import wave
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioForensicTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Audio Forensic Analysis Tool")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # Top Control Frame
        self.top_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_import = tk.Button(self.top_frame, text="Load Audio File (.wav)", command=self.load_file, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.btn_import.pack(side=tk.LEFT, padx=20)

        self.lbl_file = tk.Label(self.top_frame, text="No file loaded", font=("Arial", 10, "italic"), bg="#f0f0f0", fg="#555")
        self.lbl_file.pack(side=tk.LEFT, padx=10)

        # Main Layout: Left for Metadata, Right for Visuals
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left Frame - Metadata
        self.meta_frame = tk.LabelFrame(self.main_frame, text=" Metadata Analysis ", font=("Arial", 11, "bold"), bg="white", bd=2, relief=tk.GROOVE, width=300)
        self.meta_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))


        self.txt_metadata = tk.Text(self.meta_frame, wrap=tk.WORD, font=("Consolas", 10), bg="white", bd=0)
        self.txt_metadata.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.txt_metadata.insert(tk.END, "Load a file to analyze forensic metadata...")
        self.txt_metadata.config(state=tk.DISABLED)

        # Right Frame - Plotting Area
        self.plot_frame = tk.LabelFrame(self.main_frame, text=" Signal & Frequency Evidence (Tamper Detection) ", font=("Arial", 11, "bold"), bg="white", bd=2, relief=tk.GROOVE)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 5))
        self.fig.tight_layout(pad=3.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.clear_plots()

    def clear_plots(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_title("Waveform (Amplitude vs Time)")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Amplitude")
        self.ax2.set_title("Spectrogram (Frequency vs Time)")
        self.ax2.set_xlabel("Time (s)")
        self.ax2.set_ylabel("Frequency (Hz)")
        self.canvas.draw()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if not file_path:
            return

        self.lbl_file.config(text=os.path.basename(file_path))
        self.analyze_audio(file_path)

    def analyze_audio(self, file_path):
        try:
            # 1. Extract Metadata using native wave library
            with wave.open(file_path, 'rb') as wav:
                num_channels = wav.getnchannels()
                sample_width = wav.getsampwidth()
                sample_rate = wav.getframerate()
                num_frames = wav.getnframes()
                duration = num_frames / float(sample_rate)
                compression_type = wav.getcomptype()
                compression_name = wav.getcompname()
                
                # Read raw signal data
                raw_data = wav.readframes(num_frames)
                signal = np.frombuffer(raw_data, dtype=np.int16)
                
                # Handle stereo by taking one channel for analysis
                if num_channels == 2:
                    signal = signal[::2]

            # Get generic file system data
            file_size = os.path.getsize(file_path) / (1024 * 1024) # MB
            
            # Format Metadata Display
            meta_text = (
                f"--- FILE INFORMATION ---\n"
                f"File Name: {os.path.basename(file_path)}\n"
                f"File Size: {file_size:.2f} MB\n\n"
                f"--- AUDIO PROPERTIES ---\n"
                f"Channels: {num_channels} ({'Stereo' if num_channels==2 else 'Mono'})\n"
                f"Sample Rate: {sample_rate} Hz\n"
                f"Bit Depth: {sample_width * 8} bits\n"
                f"Total Frames: {num_frames}\n"
                f"Duration: {duration:.2f} seconds\n"
                f"Compression: {compression_name} ({compression_type})\n\n"
                f"--- FORENSIC ALERT ---\n"
            )
            
            # Basic anomaly warning check
            if sample_rate != 44100 and sample_rate != 48000:
                meta_text += "⚠️ Warning: Non-standard studio sample rate. Possible re-encoding.\n"
            else:
                meta_text += "✅ Standard sampling rate detected.\n"

            self.txt_metadata.config(state=tk.NORMAL)
            self.txt_metadata.delete("1.0", tk.END)
            self.txt_metadata.insert(tk.END, meta_text)
            self.txt_metadata.config(state=tk.DISABLED)

            # 2. Plotting Evidence
            self.ax1.clear()
            self.ax2.clear()

            time_axis = np.linspace(0, duration, len(signal))
            
            # Plot Waveform
            self.ax1.plot(time_axis, signal, color='#1f77b4', alpha=0.7)
            self.ax1.set_title("Waveform (Look for sudden cuts or silence insertions)")
            self.ax1.set_xlabel("Time (seconds)")
            self.ax1.set_ylabel("Amplitude")
            self.ax1.grid(True, linestyle='--', alpha=0.5)

            # Plot Spectrogram
            # NFFT is window size; noverlap handles smoothness
            self.ax2.specgram(signal, NFFT=1024, Fs=sample_rate, noverlap=512, cmap='viridis')
            self.ax2.set_title("Spectrogram (Look for vertical lines/breaks indicating edits)")
            self.ax2.set_xlabel("Time (seconds)")
            self.ax2.set_ylabel("Frequency (Hz)")

            self.fig.tight_layout(pad=2.0)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze audio file.\nDetails: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioForensicTool(root)
    root.mainloop()
