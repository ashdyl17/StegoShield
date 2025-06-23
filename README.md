# 🛡️ StegoShield - Image Steganography App

**StegoShield** is a modern and interactive web application that allows users to hide and retrieve secret messages inside images using **XOR encryption** combined with **LSB (Least Significant Bit) steganography**. Built using **Streamlit**, the app runs in your browser with a clean, responsive UI.

---

## 🚀 Features

- 🔒 Encrypts messages with a custom key using XOR cipher
- 🖼️ Embeds hidden data directly into the pixels of an image
- 👁️ No visible distortion in the image after encoding
- 📥 Simple drag-and-drop image upload
- 🌐 Runs in the browser using Streamlit — no installation needed
- 🔓 Decode any stego image using the original key
- 🧠 Automatically detects the length of the hidden message
- 💾 One-click download of the stego image after encoding

---

## 🎯 Problem Statement

1. Insecure transmission of sensitive data is a growing risk in today's digital world.
2. Traditional encryption methods may raise suspicion due to clearly protected formats.
3. There is a lack of tools that combine encryption with visual secrecy (steganography).
4. Users need a simple, user-friendly platform to embed and retrieve data without technical expertise.
5. Existing CLI or desktop apps can be inaccessible to non-programmers or casual users.

---

## 📌 Objective

To build a secure, accessible, and aesthetically pleasing web application that enables users to secretly hide messages within images using encryption and steganographic techniques.

---

## 🧰 Tech Stack

| Component    | Technology      |
|--------------|-----------------|
| Frontend     | Streamlit (Python) |
| Image Processing | OpenCV, NumPy, PIL |
| Encryption   | XOR Cipher       |
| Steganography | LSB (Least Significant Bit) |

---

## 📦 Installation

### 🔧 Prerequisites:
- Python 3.7+
- pip (Python package installer)

### 📥 Install Required Libraries:

```bash
pip install streamlit opencv-python pillow numpy
```

### To run
```bash
streamlit run app.py
