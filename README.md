
# 🧠 OutlineIQ – Smart PDF Outline & Metadata Extractor

**OutlineIQ** is a smart and lightweight PDF processing tool built with **Streamlit**, designed to extract structured outlines (titles and headings), hyperlinks, and embedded images from PDF files. The output is generated as a clean and readable **JSON file**.

---

## ✨ Features

- 📘 Extracts PDF title and hierarchical headings (H1, H2, H3)
- 🔗 Detects and lists all hyperlinks in the PDF
- 🖼 Extracts and previews images page-wise
- 📤 Drag-and-drop PDF upload interface
- 📥 JSON download of extracted content
- 🌗 Dark-themed user interface

---

## 📁 Project Structure

```
OutlineIQ/
├── app.py                # Streamlit frontend
├── utils.py              # PDF extraction logic
├── Dockerfile            # Docker build for batch mode
├── requirements.txt      # Python dependencies
├── logo.png              # App logo
├── input/                # Sample PDF files (for Docker use)
├── output/               # Generated JSONs from input/ PDFs
└── README.md
```

---

## 🚀 How to Use

### ▶️ Run Locally (Recommended for UI Mode)

1. Install Python packages:
```bash
pip install -r requirements.txt
```

2. Start the Streamlit app:
```bash
streamlit run app.py
```

Then open the web app in your browser and upload a PDF file.

---

### 🐳 Run with Docker (Batch Conversion Mode)

If you want to convert multiple files without UI, use Docker.

1. Build the Docker image:
```bash
docker build -t outlineiq .
```

2. Run the container and process all PDFs inside `/input`:
```bash
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  outlineiq
```

Each `.pdf` file in the `input/` folder will be processed, and the results will be saved in the `output/` folder as `.json`.

✅ **Already available:**
- `input/` folder contains sample PDF files.
- `output/` contains their corresponding JSON outputs (generated using Docker).

---

## 📂 Sample JSON Output

```json
{
  "title": "Example PDF",
  "outline": [
    {"text": "Introduction", "page": 1, "level": "H1"},
    {"text": "Overview", "page": 2, "level": "H2"}
  ],
  "metadata": {
    "links": [{"page": 2, "uri": "https://example.com"}],
    "image_previews": [{"page": 3, "preview": "base64-image-data"}]
  }
}
```

---

## 👨‍💻 Author

Made with 💻 by **Himanshu  Singh Rawat**

---

