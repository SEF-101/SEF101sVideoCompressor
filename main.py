import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import threading
from tkinter import filedialog
import ffmpeg
import sys

def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and for PyInstaller) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


ctk.set_default_color_theme(resource_path("sef101-theme.json"))


class App(ctk.CTk):
    def compress_video(self, video_full_path, output_file_name, target_size, callback):
        try:
            if not video_full_path or not os.path.exists(video_full_path):
                raise FileNotFoundError("The selected file path is invalid or the file does not exist.")

            probe = ffmpeg.probe(video_full_path)
            duration = float(probe['format']['duration'])
            audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), {}).get('bit_rate', 128000))
            target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

            min_audio_bitrate = 32000
            max_audio_bitrate = 256000

            if 10 * audio_bitrate > target_total_bitrate:
                audio_bitrate = target_total_bitrate / 10
                if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                    audio_bitrate = min_audio_bitrate
                elif audio_bitrate > max_audio_bitrate:
                    audio_bitrate = max_audio_bitrate

            video_bitrate = target_total_bitrate - audio_bitrate

            i = ffmpeg.input(video_full_path)
            ffmpeg.output(i, os.devnull, **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}).overwrite_output().run(quiet=True)
            ffmpeg.output(i, output_file_name, **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}).overwrite_output().run(quiet=True)

            for log_extension in ['log', 'log.mbtree']:
                log_path = f"ffmpeg2pass-0.{log_extension}"
                if os.path.exists(log_path):
                    os.remove(log_path)

            self.after(0, callback)

        except Exception as e:
            self.after(0, lambda: CTkMessagebox(title="Error", message=str(e), icon="cancel"))

    def getOriginalVideosPath(self):
        filePath = filedialog.askopenfilename()
        self.filePathEntry.delete(0, ctk.END)
        self.filePathEntry.insert(0, filePath)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x150")
        self.minsize(400, 150)
        self.maxsize(400, 150)
        self.title("SEF101's Video Compressor")
        #self.iconbitmap("SEF_icon.ico")
 

        self.titleLabel = ctk.CTkLabel(self, text="SEF101's Video Compressor", font=("Arial Bold", 20))
        self.titleLabel.place(x=65, y=0)

        self.filePathEntry = ctk.CTkEntry(self, placeholder_text="Enter File Path or click 'Choose File'", width=250)
        self.filePathEntry.place(x=5, y=30)

        self.chooseFileButton = ctk.CTkButton(self, text="Choose File", command=self.getOriginalVideosPath)
        self.chooseFileButton.place(x=257, y=30)

        self.targetCompressionLabel = ctk.CTkLabel(self, text="Enter Target Compression Size", font=("Arial Bold", 18))
        self.targetCompressionLabel.place(x=65, y=60)

        self.targetCompressionSizeEntry = ctk.CTkEntry(self, placeholder_text="Target Size (MB)")
        self.targetCompressionSizeEntry.place(x=45, y=90)

        self.compressButton = ctk.CTkButton(self, text="Compress", command=self.compressVideo)
        self.compressButton.place(x=210, y=90)

    def compressVideo(self):
        try:
            video_full_path = self.filePathEntry.get()
            output_directory = os.path.expanduser("~/Downloads")
            output_file_name = os.path.splitext(os.path.basename(video_full_path))[0] + "_Compressed.mp4"
            output_file_path = os.path.join(output_directory, output_file_name)

            size_input = self.targetCompressionSizeEntry.get()
            if not size_input.strip():
                raise ValueError("Please enter a valid compression size.")
            target_size = int(size_input) * 1000

            CTkMessagebox(title="Compression Started", message="Waiting for compression to finish...", icon="info")

            threading.Thread(
                target=self.compress_video,
                args=(video_full_path, output_file_path, target_size, self.finish_compression),
                daemon=True
            ).start()

        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def finish_compression(self):
        CTkMessagebox(title="Finished", message="Compression completed successfully.", icon="check")

app = App()
app.mainloop()
