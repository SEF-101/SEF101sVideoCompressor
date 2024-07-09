import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Video Compressor")

        self.compressButton = ctk.CTkButton(self, text="Compress", command=self.compressVideo)
        self.compressButton.pack()

    def compressVideo(self):
        print("Compressing Video")


app = App()
app.mainloop()