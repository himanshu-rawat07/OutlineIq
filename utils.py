import fitz  # PyMuPDF
import io
import base64
from PIL import Image

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title = doc.metadata.get("title", "Untitled") or "Untitled"
    headings = []
    pages_with_images = set()
    links = []
    image_previews = []

    for page_num, page in enumerate(doc, start=1):
        # --- Image Detection ---
        images = page.get_images(full=True)
        if images:
            pages_with_images.add(page_num)
            try:
                xref = images[0][0]  # first image only
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                img.thumbnail((100, 100))

                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                img_b64 = base64.b64encode(buffer.getvalue()).decode()

                image_previews.append({
                    "page": page_num,
                    "preview": f"data:image/png;base64,{img_b64}"
                })
            except Exception as e:
                print(f"Error generating image preview on page {page_num}: {e}")

        # --- Link Detection ---
        for link in page.get_links():
            if "uri" in link:
                links.append({
                    "page": page_num,
                    "uri": link["uri"]
                })

        # --- Heading Detection ---
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_text = " ".join(span["text"] for span in line["spans"]).strip()
                    if not line_text:
                        continue
                    max_font = max(span["size"] for span in line["spans"])
                    if max_font > 18:
                        level = "H1"
                    elif max_font > 14:
                        level = "H2"
                    elif max_font > 10:
                        level = "H3"
                    else:
                        continue
                    headings.append({
                        "level": level,
                        "text": line_text,
                        "page": page_num
                    })

    metadata = {
        "pages_with_images": sorted(list(pages_with_images)),
        "links": links,
        "image_previews": image_previews
    }

    return title, headings, metadata
