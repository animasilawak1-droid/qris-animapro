import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import requests
from io import BytesIO

# --- KONFIGURASI TEMA ---
st.set_page_config(page_title="AnimaPro QRIS", page_icon="🔴")
st.markdown("""
    <style>
    .stApp {background-color: #2e004e;} /* Warna latar belakang ungu */
    h1 {color: #ffffff; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 ANIMAPRO STUDIO")

# 1. Load Template Polos (Link Drive)
TEMPLATE_URL = "https://drive.google.com/uc?export=view&id=1eRilGjbfZkEkGmwtS2crM5jCXRsT5Vd6"

def load_template(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

template = load_template(TEMPLATE_URL)

# 2. Upload File
uploaded_file = st.file_uploader("Pilih file QR:", type=["png", "jpg"])

# 3. Logika Tampilan (Jika ada file, proses. Jika tidak, tampilkan template kosong)
if uploaded_file:
    input_img = Image.open(uploaded_file)
    detected = decode(input_img)
    
    if detected:
        (x, y, w, h) = detected[0].rect
        qr_only = input_img.crop((x, y, x + w, y + h)).resize((480, 480))
        
        final_img = template.copy()
        final_img.paste(qr_only, (265, 395)) # Koordinat yang sudah kita sesuaikan
        
        st.image(final_img, caption="Hasil QRIS AnimaPro", use_container_width=True)
        
        buf = BytesIO()
        final_img.save(buf, format="PNG")
        st.download_button("📥 DOWNLOAD QRIS", buf.getvalue(), "QRIS_AnimaPro.png", "image/png")
    else:
        st.error("QR tidak terbaca!")
else:
    # Ini yang membuat aplikasi terlihat "polos" saat awal
    st.image(template, caption="Template Kosong", use_container_width=True)
  
