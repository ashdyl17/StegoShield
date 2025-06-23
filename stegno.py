import cv2
import numpy as np
import os
import streamlit as st
import io
from PIL import Image

c2a = {chr(i): i for i in range(255)}
a2c = {i: chr(i) for i in range(255)}

def lock(msg, k):
    res = []
    for i, ch in enumerate(msg):
        res.append(c2a[ch] ^ c2a[k[i % len(k)]])
    return res

def unlock(data, k):
    out = ''
    for i, val in enumerate(data):
        out += a2c[val ^ c2a[k[i % len(k)]]]
    return out

def to_bin(data):
    return ''.join(f"{i & 0xFF:08b}" for i in data)

def hide_bits(img, bits):
    flat = img.flatten()
    if len(bits) > len(flat):
        raise ValueError("Too much data")
    for i in range(len(bits)):
        flat[i] = (flat[i] & 0xFE) | int(bits[i])
    return flat.reshape(img.shape)

def fetch_bits(img, count):
    needed = count * 8
    flat = img.flatten()
    bits = [str(flat[i] & 1) for i in range(needed)]
    return [int(''.join(bits[i:i+8]), 2) for i in range(0, needed, 8)]

st.set_page_config(page_title="Steganography App", layout="centered")
st.title("🕵️‍♂️ Steganography App")
st.markdown("Hide secret text messages inside images")

st.info("""
**About the Project:**  
This app allows you to securely hide (encode) and retrieve (decode) secret messages within images using steganography techniques. 
Developed by Ashley Dylan.
""")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Helvetica Neue', sans-serif;
        background-color: #f8f8f8;
        color: #f5f5f7 !important;
    }
    textarea, input, .stTextInput input, .stTextArea textarea {
        background-color: #1c1c1e !important;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #333 !important;
        color: #f5f5f7 !important;
    }
    .stButton > button {
        background: linear-gradient(145deg, #007aff, #0051a8);
        color: white !important;
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(145deg, #0051a8, #007aff);
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .stRadio > div {
        background-color: #2c2c2e !important;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
        color: white !important;
    }
    .stRadio > div > label {
        color: white !important;
    }
    .stDownloadButton > button {
        border-radius: 8px;
        background-color: #34c759;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PNG/JPG image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(image[:, :, ::-1], caption="Uploaded Image", use_container_width=True)

    action = st.radio("Choose Action", ["Encode", "Decode"])

    if action == "Encode":
        secret = st.text_area("Enter the message to hide")
        key = st.text_input("Key (for locking/unlocking)", type="password")
        if st.button("🔒 Encode and Download Stego Image"):
            try:
                data = [len(secret)] + lock(secret, key)
                bits = to_bin(data)
                new_img = hide_bits(image.copy(), bits)
                _, buf = cv2.imencode(".png", new_img)
                st.download_button("Download Stego Image", buf.tobytes(), file_name="stego.png", mime="image/png")
            except Exception as e:
                st.error(f"Error: {e}")

    elif action == "Decode":
        decode_key = st.text_input("Key (for unlocking)", type="password")
        if st.button("🔓 Reveal Hidden Message"):
            try:
                bits = fetch_bits(image, 1)
                ln = bits[0]
                bits = fetch_bits(image, ln + 1)[1:]
                msg = unlock(bits, decode_key)
                st.success(f"🔓 Hidden Message: `{msg}`")
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.markdown("""<hr><p style='text-align:center'>© 2025 Ashley Dylan. All rights reserved.</p>""", unsafe_allow_html=True)