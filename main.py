import os
import json
import time
from utils import extract_outline

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}")
            title, outline, metadata = extract_outline(filepath)

            output_data = {
                "title": title,
                "outline": outline,
                "metadata": metadata
            }

            out_file = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(out_file, "w") as f:
                json.dump(output_data, f, indent=2)

    print("✅ All files processed.")

if __name__ == "__main__":
    start = time.time()
    main()
    print("⏱ Finished in", round(time.time() - start, 2), "seconds")
