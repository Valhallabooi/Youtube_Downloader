import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox

def download():
    url = url_entry.get()
    # Check if the URL is still the placeholder text
    if url == "Enter YouTube URL here...":
        messagebox.showerror("Error", "Please enter a valid YouTube URL.")
        return
        
    format_choice = format_var.get()
    save_path = filedialog.askdirectory()  # Select output folder

    if not url or not save_path:
        messagebox.showerror("Error", "Please enter a URL and select a folder.")
        return

    ydl_opts = {
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",
    }

    if format_choice == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    elif format_choice == "mp4":
        ydl_opts.update({'format': 'bestvideo+bestaudio/best'})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download Complete!")
        
        # Ask if user wants to download more or exit
        ask_continue()
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {e}")
        
        # Even if download fails, ask if user wants to try again or exit
        ask_continue()

def ask_continue():
    # Create a new window for the prompt
    continue_window = tk.Toplevel(root)
    continue_window.title("Continue?")
    continue_window.geometry("300x150")
    continue_window.attributes('-topmost', True)
    
    # Center the window
    continue_window.update_idletasks()
    width = continue_window.winfo_width()
    height = continue_window.winfo_height()
    x = (continue_window.winfo_screenwidth() // 2) - (width // 2)
    y = (continue_window.winfo_screenheight() // 2) - (height // 2)
    continue_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    tk.Label(continue_window, text="Do you want to download more?", font=("Arial", 12)).pack(pady=10)
    
    # Buttons frame
    btn_frame = tk.Frame(continue_window)
    btn_frame.pack(pady=10)
    
    # Continue button
    def on_continue():
        continue_window.destroy()
        url_entry.delete(0, tk.END)  # Clear the URL field
        url_entry.insert(0, "Enter YouTube URL here...")  # Insert placeholder text
        url_entry.config(fg="white")  # Set gray color for placeholder
        
    # Exit button
    def on_exit():
        continue_window.destroy()
        root.destroy()  # Close the main program
        
    tk.Button(btn_frame, text="Yes, continue", command=on_continue, width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="No, exit", command=on_exit, width=15).pack(side=tk.LEFT, padx=5)

# Functions to handle placeholder text behavior
def on_entry_click(event):
    """Function that gets called whenever entry is clicked"""
    if url_entry.get() == "Enter YouTube URL here...":
        url_entry.delete(0, tk.END)  # Delete all the text in the entry
        url_entry.config(fg="gray")  # Change text color to black

def on_focus_out(event):
    """Function that gets called whenever entry loses focus"""
    if url_entry.get() == "":
        url_entry.insert(0, "Enter YouTube URL here...")
        url_entry.config(fg="gray")

# Create GUI window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x200")
root.attributes('-topmost', True)

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50, fg="gray")
url_entry.pack(pady=5)
url_entry.insert(0, "Enter YouTube URL here...")  # Insert placeholder text
# Bind events to the entry field
url_entry.bind("<FocusIn>", on_entry_click)
url_entry.bind("<FocusOut>", on_focus_out)

format_var = tk.StringVar(value="mp4")
tk.Label(root, text="Select Format:").pack(pady=5)
tk.Radiobutton(root, text="MP4 (Video)", variable=format_var, value="mp4").pack()
tk.Radiobutton(root, text="MP3 (Audio)", variable=format_var, value="mp3").pack()

tk.Button(root, text="Download", command=download).pack(pady=10)

root.mainloop()
