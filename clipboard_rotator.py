import tkinter as tk
from tkinter import messagebox
import tempfile
import os
import subprocess
import sys
import json
import keyboard
import time
import pystray
from PIL import Image as PILImage
import threading
import winshell
from win32com.client import Dispatch

# ---------------------------------------------------------------------------
# Config / shortcut persistence
# ---------------------------------------------------------------------------

DEFAULT_SHORTCUTS = {
    'left': 'ctrl+shift+1',
    'right': 'ctrl+shift+2',
    '180': 'ctrl+shift+3',
}

def get_config_path():
    """Return path to the JSON config file stored in %APPDATA%."""
    app_data = os.environ.get('APPDATA', os.path.expanduser('~'))
    config_dir = os.path.join(app_data, 'ClipboardRotator')
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, 'shortcuts.json')

def load_shortcuts():
    """Load shortcuts from config file, falling back to defaults."""
    try:
        with open(get_config_path(), 'r') as f:
            data = json.load(f)
        # Ensure all keys exist
        shortcuts = dict(DEFAULT_SHORTCUTS)
        shortcuts.update({k: v for k, v in data.items() if k in DEFAULT_SHORTCUTS})
        return shortcuts
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(DEFAULT_SHORTCUTS)

def save_shortcuts_to_file(shortcuts):
    """Persist shortcuts to config file."""
    try:
        with open(get_config_path(), 'w') as f:
            json.dump(shortcuts, f, indent=2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save shortcuts:\n{str(e)}")

# Active shortcuts (mutable dict used everywhere)
shortcuts = load_shortcuts()

# ---------------------------------------------------------------------------
# Auto-start helpers
# ---------------------------------------------------------------------------

def get_startup_shortcut_path():
    """Get the path to the startup shortcut"""
    startup_folder = winshell.startup()
    return os.path.join(startup_folder, "Clipboard Rotator.lnk")

def get_executable_path():
    """Get the path to the current executable or script"""
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(__file__)

def is_autostart_enabled():
    """Check if auto-start is enabled"""
    return os.path.exists(get_startup_shortcut_path())

def enable_autostart():
    """Add application to Windows startup"""
    try:
        shortcut_path = get_startup_shortcut_path()
        target_path = get_executable_path()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.Description = "Clipboard Image Rotator with Global Hotkeys"
        shortcut.save()
        
        messagebox.showinfo("Success", "Auto-start enabled!\n\nClipboard Rotator will start automatically when Windows boots.")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to enable auto-start:\n{str(e)}")
        return False

def disable_autostart():
    """Remove application from Windows startup"""
    try:
        shortcut_path = get_startup_shortcut_path()
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            messagebox.showinfo("Success", "Auto-start disabled.\n\nClipboard Rotator will not start automatically.")
        else:
            messagebox.showinfo("Info", "Auto-start was not enabled.")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disable auto-start:\n{str(e)}")
        return False

def toggle_autostart():
    """Toggle auto-start on/off"""
    if is_autostart_enabled():
        disable_autostart()
    else:
        enable_autostart()
    update_autostart_button()

def update_autostart_button():
    """Update the auto-start button text"""
    if is_autostart_enabled():
        btn_autostart.config(text="✓ Auto-Start Enabled", bg="#90EE90")
    else:
        btn_autostart.config(text="Enable Auto-Start", bg="SystemButtonFace")

# ---------------------------------------------------------------------------
# Shortcut settings dialog
# ---------------------------------------------------------------------------

def open_shortcut_settings():
    """Open a dialog that lets the user record new global hotkeys."""
    dialog = tk.Toplevel(root)
    dialog.title("Change Shortcuts")
    dialog.geometry("430x230")
    dialog.resizable(False, False)
    dialog.grab_set()  # modal

    tk.Label(dialog, text="Press the 'Record' button, then press your desired key combination.",
             wraplength=410, justify=tk.LEFT, fg='gray').pack(padx=10, pady=(10, 6))

    actions = [
        ('left',  'Rotate Left  (90°)'),
        ('right', 'Rotate Right (90°)'),
        ('180',   'Rotate 180°       '),
    ]

    entries = {}

    for key, label in actions:
        row = tk.Frame(dialog)
        row.pack(fill=tk.X, padx=10, pady=4)

        tk.Label(row, text=label, width=18, anchor='w').pack(side=tk.LEFT)

        entry = tk.Entry(row, width=22)
        entry.insert(0, shortcuts[key])
        entry.pack(side=tk.LEFT, padx=5)
        entries[key] = entry

        def make_record_handler(k, e):
            def record():
                e.delete(0, tk.END)
                e.insert(0, "Press keys…")
                e.config(bg="#FFF9C4")

                def capture():
                    try:
                        hotkey = keyboard.read_hotkey(suppress=False)
                    except Exception:
                        hotkey = shortcuts[k]
                    root.after(0, lambda: _update_entry(e, hotkey))

                threading.Thread(target=capture, daemon=True).start()
            return record

        tk.Button(row, text="Record", width=7,
                  command=make_record_handler(key, entry)).pack(side=tk.LEFT)

    def _update_entry(e, value):
        e.delete(0, tk.END)
        e.insert(0, value)
        e.config(bg="white")

    def save():
        new_shortcuts = {k: v.get().strip() for k, v in entries.items()}
        # Validate: no two shortcuts can be the same
        values = list(new_shortcuts.values())
        if len(values) != len(set(values)):
            messagebox.showerror("Error", "Each shortcut must be unique!", parent=dialog)
            return
        shortcuts.update(new_shortcuts)
        save_shortcuts_to_file(shortcuts)
        register_hotkeys()
        dialog.destroy()
        messagebox.showinfo("Saved", "Shortcuts updated successfully!")

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=8)
    tk.Button(btn_frame, text="Save", command=save, bg="#90EE90", width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=10).pack(side=tk.LEFT, padx=5)

# ---------------------------------------------------------------------------
# Shortcuts info popup
# ---------------------------------------------------------------------------

def show_shortcuts_info():
    """Show current keyboard shortcuts"""
    info = f"""Keyboard Shortcuts:

🔄 Rotation Shortcuts:
• {shortcuts['left']} → Rotate Left (90°)
• {shortcuts['right']} → Rotate Right (90°)
• {shortcuts['180']} → Rotate 180°

💡 How it works:
1. Select or hover over any image
2. Press the shortcut key
3. Image is auto-copied & rotated!

✨ Works system-wide - even when minimized!

Note: Run as administrator for best results."""

    messagebox.showinfo("Keyboard Shortcuts", info)

# ---------------------------------------------------------------------------
# Hotkey registration
# ---------------------------------------------------------------------------

def register_hotkeys():
    """Unregister all hotkeys and re-register from the current shortcuts dict."""
    keyboard.unhook_all()
    keyboard.add_hotkey(shortcuts['left'],  lambda: copy_and_rotate(90))
    keyboard.add_hotkey(shortcuts['right'], lambda: copy_and_rotate(-90))
    keyboard.add_hotkey(shortcuts['180'],   lambda: copy_and_rotate(180))

# ---------------------------------------------------------------------------
# Image rotation
# ---------------------------------------------------------------------------

def copy_and_rotate(angle):
    """Simulate Ctrl+C then rotate the image"""
    keyboard.release('shift')
    keyboard.release('ctrl')
    time.sleep(0.05)
    keyboard.send('ctrl+c')
    time.sleep(0.1)
    rotate_and_show(angle)

def get_clipboard_image():
    """Get image from clipboard with optimized imports"""
    try:
        from PIL import ImageGrab, Image
        data = ImageGrab.grabclipboard()
        if isinstance(data, Image.Image):
            return data
        elif isinstance(data, list) and data:
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
        max_size = 2000
        if img.width > max_size or img.height > max_size:
            from PIL import Image
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        rotated = img.rotate(angle, expand=True)
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            rotated.save(tmp_file.name, 'PNG', optimize=True)
            
            if sys.platform == "win32":
                os.startfile(tmp_file.name)
            elif sys.platform == "darwin":
                subprocess.run(["open", tmp_file.name])
            else:
                subprocess.run(["xdg-open", tmp_file.name])
                
    except Exception as e:
        messagebox.showerror("Error", f"Failed to rotate image: {str(e)}")

# ---------------------------------------------------------------------------
# System tray
# ---------------------------------------------------------------------------

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
    icon_image = None
    
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    icon_path = os.path.join(base_path, 'icon.ico')
    
    if os.path.exists(icon_path):
        try:
            icon_image = PILImage.open(icon_path)
        except Exception as e:
            print(f"Failed to load icon: {e}")
    
    if icon_image is None:
        icon_image = PILImage.new('RGB', (64, 64), color='blue')
    
    # Use callable titles so labels always reflect the current shortcuts
    menu = pystray.Menu(
        pystray.MenuItem('Show Window', show_window, default=True),
        pystray.MenuItem(
            lambda item: f'Rotate Left ({shortcuts["left"]})',
            lambda icon, item: copy_and_rotate(90)),
        pystray.MenuItem(
            lambda item: f'Rotate Right ({shortcuts["right"]})',
            lambda icon, item: copy_and_rotate(-90)),
        pystray.MenuItem(
            lambda item: f'Rotate 180° ({shortcuts["180"]})',
            lambda icon, item: copy_and_rotate(180)),
        pystray.MenuItem('Quit', quit_app)
    )
    
    icon = pystray.Icon("clipboard_rotator", icon_image, "Clipboard Rotator", menu)
    icon.run()

# ---------------------------------------------------------------------------
# GUI setup
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title("Clipboard Rotator")
root.geometry("350x400")

tk.Label(root, text="Clipboard Image Rotator", font=('Arial', 12, 'bold')).pack(pady=10)

# Rotation buttons frame
frame = tk.Frame(root)
frame.pack(pady=5)

btn_left = tk.Button(frame, text="Rotate Left", command=lambda: rotate_and_show(90), width=12)
btn_left.pack(side=tk.LEFT, padx=5)

btn_right = tk.Button(frame, text="Rotate Right", command=lambda: rotate_and_show(-90), width=12)
btn_right.pack(side=tk.LEFT, padx=5)

btn_180 = tk.Button(root, text="Rotate 180°", command=lambda: rotate_and_show(180), width=25)
btn_180.pack(pady=5)

# Keyboard shortcuts info button
btn_shortcuts = tk.Button(root, text="⌨ View Keyboard Shortcuts", command=show_shortcuts_info,
                          width=25, bg="#E3F2FD")
btn_shortcuts.pack(pady=5)

# Change shortcuts button
btn_change_shortcuts = tk.Button(root, text="⚙ Change Shortcut Keys", command=open_shortcut_settings,
                                 width=25, bg="#FFF3E0")
btn_change_shortcuts.pack(pady=5)

# Auto-start button
btn_autostart = tk.Button(root, text="Enable Auto-Start", command=toggle_autostart, width=25)
btn_autostart.pack(pady=5)

# Minimize to tray button
btn_minimize = tk.Button(root, text="Minimize to Tray", command=hide_window, width=25)
btn_minimize.pack(pady=5)

# Status label
tk.Label(root, text="App running in system tray", font=('Arial', 8), fg='gray').pack(pady=5)

# Update auto-start button state
update_autostart_button()

# Handle window close button to minimize to tray instead of quitting
root.protocol('WM_DELETE_WINDOW', hide_window)

# Register global hotkeys
register_hotkeys()

# Start system tray icon in a separate thread
tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
tray_thread.start()

# Start minimized to tray
root.withdraw()

root.mainloop()
