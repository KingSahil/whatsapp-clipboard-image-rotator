# WhatsApp Clipboard Image Rotator

A simple and lightweight desktop application that allows you to quickly rotate images from your clipboard - perfect for fixing those sideways photos before sharing them on WhatsApp or other platforms!

## ✨ Features

- **Instant Rotation**: Copy any image to your clipboard and rotate it with a single click
- **Multiple Rotation Options**: 
  - Rotate Left (90° counterclockwise)
  - Rotate Right (90° clockwise)  
  - Rotate 180°
- **Automatic Display**: Rotated images open automatically in your default image viewer
- **Lightweight**: Simple GUI with minimal resource usage
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Using the Executable (Windows)

1. Download the latest `clipboard_rotator.exe` from the releases
2. Run the executable - no installation required!
3. Copy an image to your clipboard (Ctrl+C)
4. Click the desired rotation button
5. The rotated image will open automatically

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
pip install pillow
```

3. Run the application:
```bash
python clipboard_rotator.py
```

## 🎯 How to Use

1. **Copy an image**: 
   - Take a screenshot (Windows: Win+Shift+S)
   - Copy an image file (right-click → copy)
   - Copy an image from a webpage or document

2. **Open the rotator**: Run the application

3. **Rotate**: Click one of the rotation buttons:
   - **Rotate Left**: 90° counterclockwise
   - **Rotate Right**: 90° clockwise
   - **Rotate 180°**: Flip upside down

4. **View result**: The rotated image opens automatically in your default image viewer

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

- **System Requirements**:
  - Windows 7+ / macOS 10.12+ / Linux with GUI
  - 50MB free space
  - Clipboard access permissions

## 🐛 Troubleshooting

**"No image in clipboard!" message?**
- Make sure you've copied an image (not text or files)
- Try copying the image again
- Some applications may not put images in clipboard format - try saving and copying the file instead

**Application won't start?**
- Ensure Python is installed correctly
- Check that Pillow is installed: `pip install pillow`
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
- Icon created for the application

---

**Made with ❤️ for the WhatsApp community and anyone tired of sideways photos!**
