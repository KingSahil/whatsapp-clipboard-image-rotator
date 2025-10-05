import tkinter as tk
from tkinter import messagebox
import tempfile
import os
import subprocess
import sys
import keyboard
import time
import pystray
from PIL import Image as PILImage
import threading

def copy_and_rotate(angle):
    """Simulate Ctrl+C then rotate the image"""
    # Simulate Ctrl+C to copy selected content
    keyboard.send('ctrl+c')
    
    # Wait a moment for clipboard to update
    time.sleep(0.1)
    
    # Now rotate the image
    rotate_and_show(angle)

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

# System tray functions
def show_window(icon=None, item=None):
    """Show the main window"""
    root.deiconify()
    root.lift()
    root.focus_force()

def hide_window():
    """Hide the main window"""
    root.withdraw()

def quit_app(icon=None, item=None):
    """Quit the application"""
    keyboard.unhook_all()
    if icon:
        icon.stop()
    root.quit()

def create_tray_icon():
    """Create system tray icon"""
    # Try to load icon.ico from multiple possible locations
    icon_image = None
    
    # Get the base path (works for both script and PyInstaller executable)
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    icon_path = os.path.join(base_path, 'icon.ico')
    
    # Try to load the icon
    if os.path.exists(icon_path):
        try:
            icon_image = PILImage.open(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {e}")
    
    # Fallback to a simple colored icon if loading fails
    if icon_image is None:
        icon_image = PILImage.new('RGB', (64, 64), color='blue')
    
    menu = pystray.Menu(
        pystray.MenuItem('Show Window', show_window, default=True),
        pystray.MenuItem('Rotate Left (Ctrl+Shift+←)', lambda: copy_and_rotate(90)),
        pystray.MenuItem('Rotate Right (Ctrl+Shift+→)', lambda: copy_and_rotate(-90)),
        pystray.MenuItem('Rotate 180° (Ctrl+Shift+↓)', lambda: copy_and_rotate(180)),
        pystray.MenuItem('Quit', quit_app)
    )
    
    icon = pystray.Icon("clipboard_rotator", icon_image, "Clipboard Rotator", menu)
    icon.run()

root = tk.Tk()
root.title("Clipboard Rotator")
root.geometry("300x200")

tk.Label(root, text="Copy an image → Click button → Instantly rotates").pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

btn_left = tk.Button(frame, text="Rotate Left", command=lambda: rotate_and_show(90))
btn_left.pack(side=tk.LEFT, padx=5)

btn_right = tk.Button(frame, text="Rotate Right", command=lambda: rotate_and_show(-90))
btn_right.pack(side=tk.LEFT, padx=5)

btn_180 = tk.Button(root, text="Rotate 180°", command=lambda: rotate_and_show(180))
btn_180.pack(pady=5)

tk.Label(root, text="Hotkeys: Ctrl+Shift+Arrow (auto-copies & rotates)", font=('Arial', 8)).pack(pady=5)

btn_minimize = tk.Button(root, text="Minimize to Tray", command=hide_window)
btn_minimize.pack(pady=5)

# Handle window close button to minimize to tray instead of quitting
root.protocol('WM_DELETE_WINDOW', hide_window)

# Register global hotkeys that auto-copy then rotate
keyboard.add_hotkey('ctrl+shift+left', lambda: copy_and_rotate(90))
keyboard.add_hotkey('ctrl+shift+right', lambda: copy_and_rotate(-90))
keyboard.add_hotkey('ctrl+shift+down', lambda: copy_and_rotate(180))

# Start system tray icon in a separate thread
tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
tray_thread.start()

# Start minimized to tray
root.withdraw()

root.mainloop()
