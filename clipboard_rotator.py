import tkinter as tk
from tkinter import messagebox
import tempfile
import os
import subprocess
import sys

def get_clipboard_image():
    """Get image from clipboard with optimized imports"""
    try:
        from PIL import ImageGrab, Image
        data = ImageGrab.grabclipboard()
        if isinstance(data, Image.Image):
            return data
        elif isinstance(data, list) and data:
            # Only try first file to avoid unnecessary loops
            try:
                return Image.open(data[0])
            except Exception:
                pass
    except ImportError:
        messagebox.showerror("Error", "PIL library not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get clipboard image: {str(e)}")
    return None

def rotate_and_show(angle):
    """Rotate image and show with optimized performance"""
    img = get_clipboard_image()
    if img is None:
        messagebox.showwarning("Warning", "No image in clipboard!")
        return
    
    try:
        # Optimize for large images - resize if too big
        max_size = 2000
        if img.width > max_size or img.height > max_size:
            from PIL import Image
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        rotated = img.rotate(angle, expand=True)
        
        # Save to temp file and open with default viewer (faster than PIL show)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            rotated.save(tmp_file.name, 'PNG', optimize=True)
            
            # Open with default system viewer
            if sys.platform == "win32":
                os.startfile(tmp_file.name)
            elif sys.platform == "darwin":
                subprocess.run(["open", tmp_file.name])
            else:
                subprocess.run(["xdg-open", tmp_file.name])
                
    except Exception as e:
        messagebox.showerror("Error", f"Failed to rotate image: {str(e)}")

root = tk.Tk()
root.title("Clipboard Rotator")
root.geometry("300x150")

tk.Label(root, text="Copy an image → Click button → Instantly rotates").pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

btn_left = tk.Button(frame, text="Rotate Left", command=lambda: rotate_and_show(90))
btn_left.pack(side=tk.LEFT, padx=5)

btn_right = tk.Button(frame, text="Rotate Right", command=lambda: rotate_and_show(-90))
btn_right.pack(side=tk.LEFT, padx=5)

btn_180 = tk.Button(root, text="Rotate 180°", command=lambda: rotate_and_show(180))
btn_180.pack(pady=5)

root.mainloop()
