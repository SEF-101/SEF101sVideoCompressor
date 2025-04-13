import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import threading
from tkinter import filedialog
import ffmpeg
import argparse

ctk.set_default_color_theme("sef101-theme.json")

def compress_video(video_full_path, output_file_name, target_size_mb, on_done=None):
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    duration = float(probe['format']['duration'])
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), {}).get('bit_rate', 128000))
    target_total_bitrate = (target_size_mb * 1024 * 8) / (1.073741824 * duration)

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

    if on_done:
        on_done()

class App(ctk.CTk):
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
            target_size = int(self.targetCompressionSizeEntry.get())

            CTkMessagebox(title="Compression Started", message="Waiting for compression to finish...", icon="info")

            threading.Thread(
                target=compress_video,
                args=(video_full_path, output_file_path, target_size, self.finish_compression),
                daemon=True
            ).start()
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def finish_compression(self):
        CTkMessagebox(title="Done", message="Compression finished successfully!", icon="check")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress a video to a target size (MB).")
    parser.add_argument("--input", help="Path to input video")
    parser.add_argument("--size", type=int, help="Target size in MB (default: 8MB)")

    args = parser.parse_args()

    if args.input:
        input_path = args.input
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.expanduser(f"~/Downloads/{base_name}_Compressed.mp4")
        target_size = args.size if args.size else 8

        try:
            print(f"Compressing {input_path} to {output_path} with target size {target_size}MB...")
            compress_video(input_path, output_path, target_size)
            print("Done!")
        except Exception as e:
            print(f"Error: {e}")
    else:
        app = App()
        app.mainloop()
