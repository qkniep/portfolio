#!/usr/bin/env python3
import os
import sys
import urllib.request
import fitz  # PyMuPDF


def generate_preview(pdf_url, output_path, paper_slug):
    temp_pdf = f"/tmp/{paper_slug}.pdf"

    print(f"Downloading {pdf_url}...")
    try:
        urllib.request.urlretrieve(pdf_url, temp_pdf)
    except Exception as e:
        print(f"Failed to download: {e}")
        return False

    print(f"Rendering first page...")
    try:
        doc = fitz.open(temp_pdf)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x resolution for crisp text
        pix.save(output_path)
        doc.close()
        os.remove(temp_pdf)
        print(f"Saved to {output_path}")
        return True
    except Exception as e:
        print(f"Failed to render: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: generate_preview.py <pdf_url> <output_path> <paper_slug>")
        sys.exit(1)

    pdf_url = sys.argv[1]
    output_path = sys.argv[2]
    paper_slug = sys.argv[3]

    generate_preview(pdf_url, output_path, paper_slug)
