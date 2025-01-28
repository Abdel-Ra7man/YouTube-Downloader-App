import yt_dlp
import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def download_video(url, save_path):
    try:
        ydl_opts = {
            "outtmpl": f"{save_path}/%(title)s.%(ext)s",  # Output template for filename
            "format": "bestvideo[height<=1080]+bestaudio/best",  # Download best video and best audio
            "noplaylist": True,  # Avoid downloading playlists
            "quiet": False,  # Show logs to debug if necessary
        }

        # Download video and audio streams
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

        # Get the filenames for video and audio (properly using the correct format extensions)
        video_filename = f"{save_path}/{info_dict['title']}.f{info_dict['formats'][0]['format_id']}.mp4"
        audio_filename = f"{save_path}/{info_dict['title']}.f{info_dict['formats'][1]['format_id']}.webm"

        # Check if files exist
        if not os.path.exists(video_filename) or not os.path.exists(audio_filename):
            messagebox.showerror("Error", "Failed to download video or audio files.")
            return

        # Merge video and audio using FFmpeg
        output_filename = f"{save_path}/{info_dict['title']}.mp4"
        merge_command = [
            "ffmpeg",
            "-i", video_filename,
            "-i", audio_filename,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "experimental",
            "-map", "0:v:0",  # Select the video stream
            "-map", "1:a:0",  # Select the audio stream
            "-y",  # Overwrite output file if it exists
            output_filename,
        ]
        subprocess.run(merge_command)

        # Remove original files
        if os.path.exists(video_filename):
            os.remove(video_filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)

        messagebox.showinfo("Success", f"Download complete: {output_filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_path_entry.delete(0, tk.END)
        save_path_entry.insert(0, folder)


def start_download():
    url = url_entry.get()
    save_path = save_path_entry.get()

    if not url.strip():
        messagebox.showerror("Error", "Please enter a video URL.")
        return

    if not save_path.strip():
        messagebox.showerror("Error", "Please select a save path.")
        return

    download_video(url, save_path)


# GUI Setup
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL Input
tk.Label(root, text="Video URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Save Path Selection
tk.Label(root, text="Save Path:").grid(row=1, column=0, padx=10, pady=10)
save_path_entry = tk.Entry(root, width=50)
save_path_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=10, pady=10)

# Download Button
tk.Button(root, text="Download", command=start_download, bg="green", fg="white").grid(
    row=2, column=1, pady=20
)

# Start the GUI event loop
root.mainloop()
