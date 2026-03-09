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

# Link Template dari Google Drive
TEMPLATE_URL = "https://drive.google.com/uc?export=view&id=1eRilGjbfZkEkGmwtS2crM5jCXRsT5Vd6"

def load_template(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except:
        return None

template = load_template(TEMPLATE_URL)

if template:
    uploaded_file = st.file_uploader("Upload Screenshot QR E-Wallet:", type=["png", "jpg"])
    
    if uploaded_file:
        input_img = Image.open(uploaded_file)
        detected = decode(input_img)
        
        if detected:
            # 1. Ambil area QR
            (x, y, w, h) = detected[0].rect
            
            # 2. Resize QR (Ubah 480 jika masih kurang pas)
            qr_only = input_img.crop((x, y, x + w, y + h)).resize((480, 480))
            
            # 3. Tempel ke template (Ubah 255/380 jika masih bergeser)
            final_img = template.copy()
            final_img.paste(qr_only, (265, 395))
            
            # Tampilkan hasil
            st.image(final_img, caption="Hasil QRIS AnimaPro", use_container_width=True)
            
            # Tombol Download
            buf = BytesIO()
            final_img.save(buf, format="PNG")
            st.download_button("📥 DOWNLOAD QRIS", buf.getvalue(), "QRIS_AnimaPro.png", "image/png")
        else:
            st.error("QR tidak terbaca. Pastikan screenshot tidak terpotong!")
else:
    st.error("Gagal memuat template. Pastikan link Drive sudah di-set 'Anyone with the link'!")
