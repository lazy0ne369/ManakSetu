import os
import re
import logging
from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF
from backend.ingestion.cleaner import clean_text

logger = logging.getLogger(__name__)


class DocumentParser:
    def __init__(self):
        # Matches patterns like "4.1 Material", "Clause 5.2.1 Operating Pressure", "6.2 High Voltage"
        self.clause_pattern = re.compile(
            r"^(?:(?:CLAUSE|Clause|Section|SECTION)\s+)?(\d+(?:\.\d+)*)\s+([A-Z][A-Za-z0-9\s,\-\(\)\/]{2,60})",
            re.MULTILINE,
        )

    def parse_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Extracts text, metadata, and pages from a PDF document using PyMuPDF."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        doc = fitz.open(file_path)
        pages_data = []

        try:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                raw_text = page.get_text("text")
                cleaned = clean_text(raw_text)
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": cleaned,
                    "raw_length": len(raw_text),
                })
        finally:
            doc.close()

        return pages_data

    def detect_clauses_in_text(self, text: str, page_number: int = 1) -> List[Dict[str, Any]]:
        """Identifies structured clauses within text."""
        sections = []
        matches = list(self.clause_pattern.finditer(text))

        if not matches:
            return [{
                "section": "General",
                "clause": "General",
                "title": "General Content",
                "page": page_number,
                "content": text.strip(),
            }]

        for i, match in enumerate(matches):
            clause_num = match.group(1).strip()
            clause_title = match.group(2).strip()
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            clause_content = text[start_pos:end_pos].strip()

            # Parent section is the primary integer prefix
            section_num = clause_num.split(".")[0] if "." in clause_num else clause_num

            sections.append({
                "section": section_num,
                "clause": clause_num,
                "title": clause_title,
                "page": page_number,
                "content": f"{clause_title}: {clause_content}" if clause_content else clause_title,
            })

        return sections
