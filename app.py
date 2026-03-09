import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import requests
from io import BytesIO

# --- KONFIGURASI TEMA ---
st.set_page_config(page_title="AnimaPro QRIS", page_icon="🔴")
st.markdown("""
    <style>
    .stApp {background-color: #ffffff;}
    h1 {color: #d32f2f; text-align: center; font-family: sans-serif;}
    .stButton>button {background-color: #d32f2f; color: white; width: 100%; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 AnimaPro Studios")
st.markdown("---")

# Fungsi ambil template dari Drive
def load_template(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# MASUKKAN DIRECT LINK DARI DRIVE KAMU DI SINI
TEMPLATE_URL = "https://drive.google.com/uc?export=download&id=1LkBijpWdh1SyM7QEnFWrL4eIagUSjq9T"

try:
    template = load_template(TEMPLATE_URL)
    
    # --- PROSES UPLOAD & EDIT ---
    uploaded_file = st.file_uploader("Upload Screenshot QR E-Wallet:", type=["png", "jpg"])
    
    if uploaded_file:
        input_img = Image.open(uploaded_file)
        detected = decode(input_img)
        
        if detected:
            # Ambil bagian QR saja
            (x, y, w, h) = detected[0].rect
            qr_only = input_img.crop((x, y, x + w, y + h)).resize((520, 520)) # Sesuaikan ukuran
            
            # Tempel ke template
            final_img = template.copy()
            final_img.paste(qr_only, (240, 360)) # Sesuaikan posisi (x, y)
            
            # Tampilkan hasil
            st.image(final_img, use_container_width=True)
            
            # Tombol Download
            buf = BytesIO()
            final_img.save(buf, format="PNG")
            st.download_button("📥 DOWNLOAD HASIL", buf.getvalue(), "QRIS_AnimaPro.png", "image/png")
        else:
            st.error("QR tidak terbaca. Pastikan screenshot tidak terpotong!")
            
except Exception as e:
    st.write("https://drive.google.com/uc?export=download&id=1LkBijpWdh1SyM7QEnFWrL4eIagUSjq9T")
