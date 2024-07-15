import customtkinter as ctk
import os
import threading
import time
from tkinter import filedialog
import ffmpeg

# class SettingsWindow(ctk.CTkToplevel):
        
#     def getOriginalVideosPath(self):
#         filePath = filedialog.askopenfilename()
#         self.outputPathEntry.delete(0,ctk.END) # remove anything in text box
#         self.outputPathEntry.insert(0,filePath) # insert filepath in text box

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.geometry("400x150")

#         self.label = ctk.CTkLabel(self, text="Change where compressed videos are saved", font=("Futura", 16))   
#         self.label.place(x=20, y=20)

#         self.outputPathEntry = ctk.CTkEntry(self, placeholder_text="Enter desired output directory or click 'Choose File'", width=250)
#         self.outputPathEntry.place(x = 5, y = 50)

#         self.chooseFileButton = ctk.CTkButton(self, text="Choose File", command=self.getOriginalVideosPath)
#         self.chooseFileButton.place(x=257, y=50)


        

class App(ctk.CTk):
    def compress_video(self, video_full_path, output_file_name, target_size, callback):
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000

        probe = ffmpeg.probe(video_full_path)
        duration = float(probe['format']['duration'])
        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), {}).get('bit_rate', 128000))
        target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate
        video_bitrate = target_total_bitrate - audio_bitrate

        log_file = "ffmpeg2pass-0.log"

        i = ffmpeg.input(video_full_path)
        ffmpeg.output(i, os.devnull, **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}).overwrite_output().run(quiet=True)
        ffmpeg.output(i, output_file_name, **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}).overwrite_output().run(quiet=True)

        # Clean up log files
        for log_extension in ['log', 'log.mbtree']:
            log_path = f"ffmpeg2pass-0.{log_extension}"
            if os.path.exists(log_path):
                os.remove(log_path)

        # Update GUI safely
        self.after(0, callback)


    def getOriginalVideosPath(self):
        filePath = filedialog.askopenfilename()
        self.filePathEntry.delete(0,ctk.END) # remove anything in text box
        self.filePathEntry.insert(0,filePath) # insert filepath in text box

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x200")
        self.minsize(400,200)
        self.maxsize(400,200)
        self.title("Video Compressor")
        self.settingsWindow = None

        self.titleLabel = ctk.CTkLabel(self, text="Video Compressor", font=("Arial Bold", 20))
        self.titleLabel.place(x = 110, y = 0)

        self.filePathEntry = ctk.CTkEntry(self, placeholder_text="Enter File Path or click 'Choose File'", width=250)
        self.filePathEntry.place(x = 5, y = 30)

        self.chooseFileButton = ctk.CTkButton(self, text="Choose File", command=self.getOriginalVideosPath)
        self.chooseFileButton.place(x=257, y=30)

        self.targetCompressionLabel = ctk.CTkLabel(self, text="Enter Target Compression Size", font=("Arial Bold", 18))
        self.targetCompressionLabel.place(x = 65, y = 60)

        self.targetCompressionSizeEntry = ctk.CTkEntry(self, placeholder_text="Target Size (MB)")
        self.targetCompressionSizeEntry.place(x = 45, y = 90)

        self.compressButton = ctk.CTkButton(self, text="Compress", command=self.compressVideo)
        self.compressButton.place(x=210, y=90)

        self.compressProgressBar = ctk.CTkProgressBar(self, width=250)
        self.compressProgressBar.set(0.0)
        self.compressProgressBar.place(x=75, y=140)

        self.percentageLabel = ctk.CTkLabel(self, text="0%")
        self.percentageLabel.place(x=335, y=130)

        # self.settingsButton = ctk.CTkButton(self, text="Settings", command=self.openSettings, width=30)
        # self.settingsButton.place(x=5, y=170)


    # def openSettings(self):
    #     if self.settingsWindow is None or not self.settingsWindow.winfo_exists():
    #         self.settingsWindow = SettingsWindow(self)  # create window if its None or destroyed
    #     else:
    #         self.settingsWindow.focus()  # if window exists focus it

    def compressVideo(self):
        video_full_path = self.filePathEntry.get()
        output_directory = os.path.expanduser("~/Downloads")
        output_file_name = os.path.splitext(os.path.basename(video_full_path))[0] + "_Compressed.mp4"
        output_file_path = os.path.join(output_directory, output_file_name)
        target_size = int(self.targetCompressionSizeEntry.get()) * 1000

        # Update GUI that compression is starting
        self.compressProgressBar.set(0)
        self.percentageLabel.configure(text="0%")

        # Start compression in a new thread
        threading.Thread(target=self.compress_video, args=(video_full_path, output_file_path, target_size, self.finish_compression), daemon=True).start()

    def finish_compression(self):
        self.compressProgressBar.set(100)
        self.percentageLabel.configure(text="Done!")


app = App()
app.mainloop()

