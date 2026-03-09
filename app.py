import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import requests
from io import BytesIO

# Memuat template
TEMPLATE_URL = "https://drive.google.com/uc?export=view&id=1eRilGjbfZkEkGmwtS2crM5jCXRsT5Vd6"

@st.cache_data
def load_template(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

template = load_template(TEMPLATE_URL)

uploaded_file = st.file_uploader("Upload QR E-Wallet:", type=["png", "jpg"])

if uploaded_file:
    input_img = Image.open(uploaded_file)
    detected = decode(input_img)
    
    if detected:
        (x, y, w, h) = detected[0].rect
        # Menentukan ukuran QR yang ideal untuk kotak tersebut
        qr_size = 480 
        qr_only = input_img.crop((x, y, x + w, y + h)).resize((qr_size, qr_size))
        
        # Koordinat pusat kotak putih template
        center_x = 485
        center_y = 635
        
        # Menghitung posisi agar QR di tengah
        pos_x = center_x - (qr_size // 2)
        pos_y = center_y - (qr_size // 2)
        
        final_img = template.copy()
        final_img.paste(qr_only, (pos_x, pos_y))
        
        st.image(final_img, use_container_width=True)
        # ... (tombol download)
      
