# Video Compressor
To use this program, you must have ffmpeg installed on your machine.

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

