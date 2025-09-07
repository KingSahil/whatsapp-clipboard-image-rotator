import tkinter as tk
from PIL import ImageGrab, Image

def get_clipboard_image():
    data = ImageGrab.grabclipboard()
    if isinstance(data, Image.Image):
        return data
    elif isinstance(data, list):
        for path in data:
            try:
                return Image.open(path)
            except:
                continue
    return None

def rotate_and_show(angle):
    img = get_clipboard_image()
    if img is None:
        print("⚠️ No image in clipboard!")
        return
    rotated = img.rotate(angle, expand=True)
    rotated.show()

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
