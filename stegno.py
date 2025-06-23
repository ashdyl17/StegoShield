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
st.title("🕵️‍♂️ StegoShield")
with st.expander("🧭 Instructions"):
    st.markdown("""
1. **Upload an Image**: Choose a `.png` or `.jpg` image where the message will be hidden.  
2. **Select Mode**: Click on either **Encode** or **Decode**.  
3. **For Encoding**:
   - Type your secret message in the box.
   - Enter a key to lock the message (only those with the key can unlock it).
   - Click the encode button to download the stego image.  
4. **For Decoding**:
   - Enter the key used during encoding.
   - Click to reveal the hidden message.
""")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, sans-serif;
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
        background: linear-gradient(to bottom, #007aff, #0051a8);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 16px;
        transition: background 0.3s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(to bottom, #0051a8, #007aff);
        box-shadow: 0 6px 16px rgba(0, 122, 255, 0.4);
        transform: scale(1.01);
    }
    .stDownloadButton > button {
        border-radius: 8px;
        background-color: #34c759;
        color: white;
        font-weight: bold;
    }
    /* Force white text for radio labels */
    @media (prefers-color-scheme: light) {
        [data-baseweb="radio"] label span {
            color: black !important;
            background-color: #e6e6e6 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PNG/JPG image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(image[:, :, ::-1], caption="Uploaded Image", use_container_width=True)

    if "mode" not in st.session_state:
        st.session_state.mode = "Encode"

    if st.button("Encode", key="enc_btn"):
        st.session_state.mode = "Encode"
    if st.button("Decode", key="dec_btn"):
        st.session_state.mode = "Decode"

    action = st.session_state.mode

    if action == "Encode":
        secret = st.text_area("Enter the message to hide")
        key = st.text_input("Key (for locking/unlocking)", type="password")
        max_capacity = image.size // 8
        if secret and len(secret) > max_capacity:
            st.error(f"Message too long! This image can hold only about {max_capacity} characters.")
            st.stop()
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

st.markdown("""<hr><p style='text-align:center'>© 2025 Ashley Dylan.</p>""", unsafe_allow_html=True)
