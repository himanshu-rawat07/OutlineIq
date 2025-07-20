import streamlit as st
import json
import os
from utils import extract_outline

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="OutlineIQ",
    page_icon="🧠",
    layout="centered"
)

# ---------- Theme Toggle ----------
theme = st.radio("🌗 Choose Theme", ["Dark", "Light"], horizontal=True)

# ---------- Dynamic Colors ----------
if theme == "Light":
    bg_color = "#f8fafc"
    text_color = "#1e293b"
    box_bg = "#ffffff"
    subtitle_color = "#475569"
else:
    bg_color = "#0f172a"
    text_color = "#ffffff"
    box_bg = "#1e293b"
    subtitle_color = "#94a3b8"

# ---------- Custom CSS Styling ----------
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            background-color: {bg_color};
            color: {text_color};
        }}

        .center {{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }}

        .logo {{
            margin-top: 1rem;
            margin-bottom: -0.5rem;
        }}

        .title {{
            font-size: 2.8rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.2rem;
        }}

        .subtitle {{
            font-size: 1.1rem;
            font-weight: 400;
            color: {subtitle_color};
            text-align: center;
            margin-bottom: 1.5rem;
        }}

        .section-title {{
            font-size: 1.4rem;
            font-weight: 600;
            color: #facc15;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}

        .outline-box {{
            background-color: {box_bg};
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }}

        .outline-item {{
            margin-left: 1rem;
            margin-bottom: 0.4rem;
        }}

        .link-item {{
            margin-bottom: 0.5rem;
        }}

        .image-block {{
            margin-bottom: 1rem;
        }}

        .stButton>button, .stDownloadButton>button {{
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }}

        hr {{
            border: none;
            border-top: 1px solid #334155;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }}
    </style>
""", unsafe_allow_html=True)

# ---------- Centered Logo and Title ----------
col = st.columns([1, 2, 1])[1]
with col:
    st.image("logo.png", width=120)
    st.markdown('<div class="title">OutlineIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart PDF Outline & Metadata Extractor</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- File Upload ----------
uploaded_file = st.file_uploader("📁 Upload your PDF file", type=["pdf"])

if uploaded_file:
    file_size = round(len(uploaded_file.read()) / 1e6, 2)
    uploaded_file.seek(0)

    with st.spinner("⏳ Processing your file..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        title, outline, metadata = extract_outline("temp.pdf")
        result = {
            "title": title,
            "outline": outline,
            "metadata": metadata
        }
        json_str = json.dumps(result, indent=2)

    st.success("✅ Extraction complete!")

    # ---------- Title Display ----------
    st.markdown(f"<div class='section-title'>📘 Title: {title or 'Untitled'}</div>", unsafe_allow_html=True)

    # ---------- Outline Display ----------
    st.markdown("<div class='section-title'>📝 Document Outline</div>", unsafe_allow_html=True)
    st.markdown("<div class='outline-box'>", unsafe_allow_html=True)
    for item in outline:
        icon = {"H1": "🔷", "H2": "🔹", "H3": "▫️"}.get(item["level"], "•")
        st.markdown(f"<div class='outline-item'>{icon} <strong>{item['text']}</strong> (Page {item['page']})</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Links Display ----------
    st.markdown("<div class='section-title'>🔗 Links Found</div>", unsafe_allow_html=True)
    if metadata["links"]:
        for link in metadata["links"]:
            st.markdown(f"<div class='link-item'>🌐 Page {link['page']} → <a href='{link['uri']}' target='_blank'>{link['uri']}</a></div>", unsafe_allow_html=True)
    else:
        st.info("No external links found.")

    # ---------- Image Previews ----------
    st.markdown("<div class='section-title'>🖼 Image Previews</div>", unsafe_allow_html=True)
    if metadata["image_previews"]:
        for img in metadata["image_previews"]:
            st.markdown(f"<div class='image-block'><strong>Page {img['page']}</strong></div>", unsafe_allow_html=True)
            st.image(img["preview"], use_column_width=True)
    else:
        st.info("No images found in this PDF.")

    # ---------- Download Button ----------
    st.download_button("📥 Download JSON", json_str, file_name="outline.json", mime="application/json")
else:
    st.warning("📂 Please upload a PDF file to begin.")
