import customtkinter as ctk
import os
from tkinter import filedialog
import ffmpeg

class App(ctk.CTk):
    filepath = ""

    def compress_video(video_full_path, output_file_name, target_size):
        # This method is taken from https://stackoverflow.com/questions/64430805/how-to-compress-video-to-target-size-by-python

        # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000

        probe = ffmpeg.probe(video_full_path)
        # Video duration, in s.
        duration = float(probe['format']['duration'])
        # Audio bitrate, in bps.
        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
        # Target total bitrate, in bps.
        target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

        # Target audio bitrate, in bps
        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate
        # Target video bitrate, in bps.
        video_bitrate = target_total_bitrate - audio_bitrate

        i = ffmpeg.input(video_full_path)
        ffmpeg.output(i, os.devnull,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                    ).overwrite_output().run()
        ffmpeg.output(i, output_file_name,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                    ).overwrite_output().run()

    def getOriginalVideosPath(self):
        filePath = filedialog.askopenfilename()
        self.filePathEntry.delete(0,ctk.END) # remove anything in text box
        self.filePathEntry.insert(0,filePath) # insert filepath in text box

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Video Compressor")

        self.filePathEntry = ctk.CTkEntry(self, placeholder_text="Enter File Path")
        self.filePathEntry.pack()

        self.chooseFileButton = ctk.CTkButton(self, text="Choose File", command=self.getOriginalVideosPath)
        self.chooseFileButton.pack()

        self.targetCompressionSizeEntry = ctk.CTkEntry(self, placeholder_text="Enter Compression Size", width=220)
        self.targetCompressionSizeEntry.pack()

        self.compressButton = ctk.CTkButton(self, text="Compress", command=self.compressVideo)
        self.compressButton.pack()

    def compressVideo(self):
        print("Compressing Video")


# app = App()
# app.mainloop()

