import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import requests
from io import BytesIO

# Konfigurasi Tampilan
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

# Mengambil template dari link Drive kamu
TEMPLATE_URL = "https://drive.google.com/uc?export=download&id=1eRilGjbfZkEkGmwtS2crM5jCXRsT5Vd"

def load_template(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

try:
    template = load_template(TEMPLATE_URL)
    
    uploaded_file = st.file_uploader("Upload Screenshot QR E-Wallet:", type=["png", "jpg"])
    
    if uploaded_file:
        input_img = Image.open(uploaded_file)
        detected = decode(input_img)
        
        if detected:
            # Mengambil area QR dan mengatur ukurannya agar pas di kotak putih
            (x, y, w, h) = detected[0].rect
            qr_only = input_img.crop((x, y, x + w, y + h)).resize((500, 500))
            
            # Menempelkan QR ke template (Posisi koordinat X: 245, Y: 365)
            # Jika kurang pas, kamu bisa ubah angka ini sedikit demi sedikit
            final_img = template.copy()
            final_img.paste(qr_only, (245, 365))
            
            # Tampilan hasil
            st.image(final_img, caption="Hasil QRIS AnimaPro", use_container_width=True)
            
            # Tombol Download
            buf = BytesIO()
            final_img.save(buf, format="PNG")
            st.download_button("📥 DOWNLOAD QRIS", buf.getvalue(), "QRIS_AnimaPro.png", "image/png")
        else:
            st.error("QR tidak terbaca. Pastikan screenshot tidak terpotong!")
            
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
  
