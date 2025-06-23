# 🛡️ StegoShield

**StegoShield** is a Python-based desktop application that hides secret text messages inside images using a combination of XOR encryption and Least Significant Bit (LSB) steganography. Built with an interactive GUI using Tkinter, it provides an easy-to-use, secure, and stealthy way to transmit confidential information.

---

## 🚀 Features

- 🔐 **Dual-layer security** using XOR encryption and LSB encoding
- 🖼️ Supports JPG and PNG image formats
- 🧠 No visible distortion to the original image
- 💬 Simple GUI to encode/decode messages without coding
- ⚙️ Fully offline — no internet required to use
- 💾 Saves the output as a new image without overwriting original
- 🧪 Lightweight and cross-platform compatible

---

## ❗ Problem Statement

- Digital communication requires protection of sensitive data from unauthorized access.
- Encryption alone may draw attention and can be detected during transmission.
- Users lack an easy-to-use tool that allows messages to be hidden in images without visible change.
- Existing methods are complex or require programming knowledge.
- There's a need for a discrete and reversible technique for secure information hiding in images.

---

## 🎯 Objective

To develop a user-friendly, secure, and efficient image-based steganography system that enables users to conceal and retrieve confidential messages without affecting the visual quality of the image.

---

## 🧰 System Requirements

- **OS**: Windows, macOS, or Linux  
- **Python**: Version 3.7 or higher  
- **RAM**: Minimum 4 GB  
- **Dependencies**:
  - `opencv-python`
  - `numpy`
  - `Pillow`
  - (Tkinter comes preinstalled with Python)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/StegoShield.git
cd StegoShield

# Install dependencies
pip install opencv-python numpy pillow
