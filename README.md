# SEF101's Video Compressor

A simple desktop tool to compress video files to a target size (in MB).  
Built with Python and CustomTkinter for a clean, lightweight experience.

> ⚠️ Requires [FFmpeg](https://ffmpeg.org/download.html) to be installed and available in your system PATH.

## Installing FFmpeg on windows:
1. Download the latest version of FFmpeg from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).
2. Unzip the downloaded file using a file archiver like Winrar or 7z.
    ![Screenshot of unzipping the folder](https://media.geeksforgeeks.org/wp-content/uploads/20210912212008/1.png)
3. Rename the extracted folder to "ffmpeg" and move it to the root of the C: drive.
    ![Screenshot of folder in C drive](https://media.geeksforgeeks.org/wp-content/uploads/20210912212010/3.png)
4. Open the command prompt as an administrator and set the environment path variable for ffmpeg by running the following command:
    ```
    setx /m PATH "C:\ffmpeg\bin;%PATH%"
    ```
    ![Screenshot of setting path](https://media.geeksforgeeks.org/wp-content/uploads/20210912212036/Screenshotfrom20210912211815.png)
5. Restart your computer and verify the installation by running the command:
    ```
    ffmpeg -version
    ```
    ![Screenshot of a verified installation](https://media.geeksforgeeks.org/wp-content/uploads/20210912212115/Screenshotfrom20210912212044.png)

FFmpeg is now installed on your machine! You can proceed to download and run the Video Compressor GUI.

## Installing Video Compressor:

You can use the app in two ways:

### Option 1: Download the EXE (Recommended for Windows users)

1. Go to the [Releases](https://github.com/SEF-101/VideoCompressor/releases) section.
2. Download the latest `.exe` file.
3. Run the file — no setup required!

> ⚠️ Windows may show a security warning. Click “More info” → “Run anyway” to trust the app.

### Option 2: Run from GitHub Repo

1. Clone the repository:
    ```bash
    git clone https://github.com/yusef800/VideoCompressor.git
    ```
2. Navigate to the project directory:
    ```bash
    cd VideoCompressor
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    python main.py
    ```

You can now use the Video Compressor by following the usage instructions below.

## Using Video Compressor:

1. **Click “Choose File”** and select the video you want to compress.

2. **Enter the target size** in megabytes (e.g., `8` for 8MB).

3. **Click “Compress”** — the app will process your video in the background.

4. The compressed file will be saved to your **Downloads** folder with `_Compressed` added to the filename.

You’ll get a popup when it’s done. That’s it!

## Supported File Formats

The Video Compressor supports a wide range of video formats for input, thanks to FFmpeg. Below are some of the commonly supported formats:

### Input Formats:
- MP4
- AVI
- MKV
- MOV
- WMV
- FLV
- WebM
- And many more (any format supported by FFmpeg).

### Output Format:
- MP4 with:
  - Video Codec: H.264 (`libx264`)
  - Audio Codec: AAC
