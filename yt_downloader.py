import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # Import ttk for Progressbar
import yt_dlp
import threading
import os

# Function to get download link and download the file
def get_download_link():
    link = video_link_entry.get().strip()  # Get the YouTube link from input field

    if not link:
        messagebox.showerror("Error", "Please enter a valid YouTube link!")
        return

    try:
        # Ask user for download path if not set
        if not download_path:
            messagebox.showerror("Error", "Please select a valid download path!")
            return
        
        choice = selected_option.get()
        
        # Define download options based on the user's choice
        if choice == "1":  # High Resolution Video
            ydl_opts = {
                'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'progress_hooks': [progress_hook],
                'outtmpl': os.path.join(download_path, '%(title)s_HighRes.%(ext)s')  # Set custom download path
            }
            option_text = "High Resolution Video"
        elif choice == "2":  # Low Resolution Video
            ydl_opts = {
                'format': 'worst',
                'progress_hooks': [progress_hook],
                'outtmpl': os.path.join(download_path, '%(title)s_LowRes.%(ext)s')  # Set custom download path
                
            }
            option_text = "Low Resolution Video"
        elif choice == "3":  # Audio Only
            ydl_opts = {
                'format': 'bestaudio[ext=mp3]/bestaudio',
                # 'format': 'bestaudio',  # Download only the best audio (no video)
                'progress_hooks': [progress_hook],
                'outtmpl': os.path.join(download_path, '%(title)s_Audio.%(ext)s')  # Set custom download path
            }
            option_text = "Audio Only"
        else:
            messagebox.showerror("Error", "Please select a valid option!")
            return

        # Start the download in a separate thread to prevent blocking the GUI
        download_thread = threading.Thread(target=download_video, args=(link, ydl_opts, option_text))
        download_thread.start()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle download
def download_video(link, ydl_opts, option_text):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)  # This will download the file
        
        title = info.get('title', 'Unknown Title')
        
        # Show the download completion message
        messagebox.showinfo("Download Completed", f"Video Title: {title}\nOption: {option_text}\nDownload completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to track download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        if d.get('total_bytes') is not None:  # Ensure we don't divide by None
            progress_var.set(d['downloaded_bytes'] / d['total_bytes'] * 100)
            root.update_idletasks()  # Update the GUI during download

# Function to allow the user to select a download path
def select_download_path():
    global download_path
    download_path = filedialog.askdirectory()  # Ask user to select directory
    if download_path:
        path_label.config(text=f"Download Path: {download_path}")

# Create main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Set window size and background color
root.geometry("700x450")
root.config(bg="#f4f4f9")

# Title label
title_label = tk.Label(root, text="YouTube Video Downloader", font=("Helvetica", 20, "bold"), bg="#f4f4f9", fg="#4CAF50")
title_label.pack(pady=20)

# Label for instructions
label = tk.Label(root, text="Enter the YouTube video link:", font=("Helvetica", 12), bg="#f4f4f9")
label.pack(pady=5)

# Entry widget to input video link
video_link_entry = tk.Entry(root, width=45, font=("Helvetica", 12))
video_link_entry.pack(pady=5)

# Variable to track selected option
selected_option = tk.StringVar(value="1")  # Default is High Resolution

# Radio buttons for options
# Create a frame to group radio buttons
radio_frame = tk.Frame(root, bg="#f4f4f9")
radio_frame.pack(pady=20, fill="both", expand=True)

# Configure grid columns for proportional spacing
radio_frame.grid_columnconfigure(0, weight=1)  # First column
radio_frame.grid_columnconfigure(1, weight=1)  # Second column
radio_frame.grid_columnconfigure(2, weight=1)  # Third column

# High Resolution Video radio button
radio_button_1 = tk.Radiobutton(
    radio_frame,
    text="High Resolution Video",
    variable=selected_option,
    value="1",
    font=("Helvetica", 12),
    bg="#81BFDA",
    relief="raised",
    width=20
)
radio_button_1.grid(row=0, column=0, padx=20, pady=5, sticky="ew")  # First button

# Low Resolution Video radio button
radio_button_2 = tk.Radiobutton(
    radio_frame,
    text="Low Resolution Video",
    variable=selected_option,
    value="2",
    font=("Helvetica", 12),
    bg="#4CC9FE",
    relief="raised",
    width=20
)
radio_button_2.grid(row=0, column=1, padx=20, pady=5, sticky="ew")  # Second button

# Audio Only radio button
radio_button_3 = tk.Radiobutton(
    radio_frame,
    text="Audio Only",
    variable=selected_option,
    value="3",
    font=("Helvetica", 12),
    bg="#0A97B0",
    relief="raised",
    width=20
)
radio_button_3.grid(row=0, column=2, padx=20, pady=5, sticky="ew")  # Third button

# Button to select download path
path_button = tk.Button(root, text="Select Download Path", command=select_download_path, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat")
path_button.pack(pady=10)

# Label to show the selected download path
path_label = tk.Label(root, text="Download Path: Not Selected", font=("Helvetica", 12), bg="#f4f4f9", fg="red")
path_label.pack(pady=5)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, length=300, mode='determinate', variable=progress_var)  # Use ttk for Progressbar
progress_bar.pack(pady=10)

# Download button
download_button = tk.Button(root, text="Download", command=get_download_link, font=("Helvetica", 12, "bold"), bg="#008CBA", fg="white", relief="flat")
download_button.pack(pady=15)

# Start the GUI event loop
root.mainloop()
