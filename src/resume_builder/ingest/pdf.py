"""Extract text from PDF files for review before DB ingestion."""
from pathlib import Path

import pdfplumber


def extract_text(pdf_path: str | Path) -> str:
    """Return all text from a PDF, page-joined by a divider."""
    path = Path(pdf_path)
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            pages.append(f"--- Page {i} ---\n{text}")
    return "\n\n".join(pages)


def extract_from_dir(directory: str | Path, pattern: str = "*.pdf") -> dict[str, str]:
    """Return a mapping of filename -> extracted text for all PDFs in a directory."""
    d = Path(directory)
    return {p.name: extract_text(p) for p in sorted(d.glob(pattern))}
