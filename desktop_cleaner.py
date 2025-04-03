import os
import shutil
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

# Define file categories
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
    'Music': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Programs': ['.exe', '.msi'],
    'Others': []  # Unclassified files
}

desktop_path = Path.home() / "Desktop"

"""Organizes files in the selected folder into categorized folders."""
def organize_files(folder_path, progress_var):
    files = list(Path(folder_path).iterdir())
    total_files = len(files)    

    for index, file in enumerate(files):
        if file.is_file():
            move_file(file)
        progress_var.set(int((index + 1) / total_files * 100))

    messagebox.showinfo("Success", "Cleaning completed!")

"""Moves a file to the allocated category folder"""
def move_file(file):
    file_extension = file.suffix.lower()
    destination_folder = "Others"

    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            destination_folder = category
            break

    target_path = file.parent / destination_folder
    target_path.mkdir(exist_ok=True)
    shutil.move(str(file), str(target_path / file.name))

def choose_folder(progress_var):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        organize_files(folder_selected, progress_var)

def add_to_startup():
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    shortcut_path = startup_folder / "DesktopCleaner.bat"

    with open(shortcut_path, "w") as shortcut:
        shortcut.write(f"python \"{script_path}\"")

    messagebox.showinfo("Startup", "Desktop Cleaner will now run on startup!")

def remove_from_startup():
    startup_folder = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    shortcut_path = startup_folder / "DesktopCleaner.bat"

    if shortcut_path.exists():
        shortcut_path.unlink()
        messagebox.showinfo("Startup", "Auto-run disabled!")
    else:
        messagebox.showwarning("Startup", "Auto-run is not enabled.")


def load_icon(filename, size=(32, 32)):
    icon_path = Path(sys.argv[0]).parent / "icons" / filename
    img = Image.open(icon_path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Create GUI
root = tk.Tk()
root.title("Desktop Cleaner")
root.geometry("500x400")
root.resizable(True, True)

# modern style
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", font=("Arial", 10))
style.configure("TLabel", font=("Arial", 12))

# Load icons
clean_icon = load_icon("clean.png")
folder_icon = load_icon("folder.png")
startup_icon = load_icon("startup.png")
disable_icon = load_icon("disable.png")
exit_icon = load_icon("exit.png")

# Main frame
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

label = ttk.Label(frame, text="Select an action:")
label.grid(row=0, column=0, columnspan=2, pady=10)

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, length=300, mode='determinate', variable=progress_var)
progress_bar.grid(row=1, column=0, columnspan=2, pady=5)

# Buttons with icons
ttk.Button(frame, text=" Clean Desktop", command=lambda: organize_files(desktop_path, progress_var), image=clean_icon, compound="left").grid(row=2, column=0, columnspan=2, pady=5, ipadx=10)
ttk.Button(frame, text=" Choose Folder", command=lambda: choose_folder(progress_var), image=folder_icon, compound="left").grid(row=3, column=0, columnspan=2, pady=5, ipadx=10)
ttk.Button(frame, text=" Enable Auto-Run", command=add_to_startup, image=startup_icon, compound="left").grid(row=4, column=0, pady=5, ipadx=10)
ttk.Button(frame, text=" Disable Auto-Run", command=remove_from_startup, image=disable_icon, compound="left").grid(row=4, column=1, pady=5, ipadx=10)
ttk.Button(frame, text=" Exit", command=root.quit, image=exit_icon, compound="left").grid(row=6, column=0, columnspan=2, pady=10, ipadx=20)

root.mainloop()