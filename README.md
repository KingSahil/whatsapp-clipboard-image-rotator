# WhatsApp Clipboard Image Rotator

A lightweight desktop application that runs in your system tray, allowing you to instantly rotate images with global hotkeys - perfect for fixing those sideways photos before sharing them on WhatsApp or other platforms!

## ✨ Features

- **🖼️ Global Hotkeys**: Rotate images from anywhere with Ctrl+Shift+Arrow keys
- **🔄 Auto-Copy & Rotate**: Select an image and press the hotkey - it copies and rotates in one action!
- **📋 System Tray**: Runs minimized in the background, always ready when you need it
- **⚡ Instant Rotation**: 
  - Rotate Left (90° counterclockwise) - **Ctrl+Shift+Left**
  - Rotate Right (90° clockwise) - **Ctrl+Shift+Right**
  - Rotate 180° - **Ctrl+Shift+Down**
- **🎨 Automatic Display**: Rotated images open automatically in your default image viewer
- **💨 Lightweight**: Minimal resource usage, works silently in the background

## 🚀 Quick Start

### Using the Executable (Windows)

1. Download the latest `clipboard_rotator.exe` from the releases
2. Run the executable - it starts minimized in the system tray!
3. **Select any image** in WhatsApp, browser, or any app
4. Press **Ctrl+Shift+Left/Right/Down** to instantly copy & rotate
5. The rotated image opens automatically

**Note**: Run as administrator for global hotkeys to work system-wide.

### Running from Source

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

#### Installation

1. Clone this repository:
```bash
git clone https://github.com/KingSahil/Whatsapp-clipboard-image-rotator.git
cd Whatsapp-clipboard-image-rotator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python clipboard_rotator.py
```

## ⌨️ Keyboard Shortcuts

The app registers **global hotkeys** that work system-wide:

- **Ctrl+Shift+Left** → Rotate Left (90° counterclockwise)
- **Ctrl+Shift+Right** → Rotate Right (90° clockwise)
- **Ctrl+Shift+Down** → Rotate 180°

💡 **Pro Tip**: Just select/hover over an image and press the hotkey - it automatically copies and rotates!

## 🎯 How to Use

### Method 1: Global Hotkeys (Recommended)

1. **Start the app**: It will run minimized in your system tray
2. **Find an image**: In WhatsApp, browser, file explorer, etc.
3. **Select the image** (hover over it or click it)
4. **Press Ctrl+Shift+Arrow** to instantly copy & rotate
5. **View result**: The rotated image opens automatically

### Method 2: Manual Copy + GUI

1. **Copy an image**: 
   - Take a screenshot (Windows: Win+Shift+S)
   - Copy an image file (right-click → copy)
   - Copy an image from a webpage or document

2. **Open the window**: Right-click the tray icon → Show Window

3. **Rotate**: Click one of the rotation buttons

4. **View result**: The rotated image opens automatically

## 🎛️ System Tray

The application runs in the system tray with these options:
- **Show Window**: Open the GUI interface
- **Rotate Left/Right/180°**: Quick rotation from tray menu
- **Quit**: Exit the application

## 🛠️ Building from Source

To create your own executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico clipboard_rotator.py
```

The executable will be created in the `dist/` folder.

## 📋 Requirements

- **Python Libraries**: 
  - `tkinter` (usually included with Python)
  - `Pillow` (PIL fork for image processing)
  - `keyboard` (for global hotkey support)
  - `pystray` (for system tray functionality)

- **System Requirements**:
  - Windows 7+ / macOS 10.12+ / Linux with GUI
  - 50MB free space
  - Clipboard access permissions
  - Administrator privileges (recommended for global hotkeys)

## 🐛 Troubleshooting

**Hotkeys not working?**
- Run the application as administrator
- Make sure no other app is using the same hotkey combination
- Check that the app is running (look for the tray icon)

**"No image in clipboard!" message?**
- Make sure you've copied or selected an image (not text or files)
- Try pressing Ctrl+C manually first, then use the rotation button
- Some applications may not support clipboard image format

**Can't find the tray icon?**
- Check the hidden icons in your system tray (click the ^ arrow)
- The app starts minimized - look for a blue icon or "Clipboard Rotator"

**Application won't start?**
- Ensure Python is installed correctly
- Install all dependencies: `pip install -r requirements.txt`
- Try running from command line to see error messages

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with Python and Tkinter for the GUI
- Image processing powered by Pillow (PIL)
- Global hotkeys via keyboard library
- System tray functionality via pystray
- Icon created for the application

## 🎮 Usage Tips

- **WhatsApp Web**: Select an image, press Ctrl+Shift+Left/Right to rotate before sending
- **Screenshots**: Capture with Win+Shift+S, then immediately rotate with hotkeys
- **File Explorer**: Select an image file and use hotkeys to quickly preview rotated version
- **Keep it running**: The app uses minimal resources in the tray - perfect for keeping it on all the time!

---

**Made with ❤️ for the WhatsApp community and anyone tired of sideways photos!**
