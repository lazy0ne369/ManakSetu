from typing import List, Dict, Any
from backend.ingestion.cleaner import clean_text


class StructureAwareChunker:
    """Structure-aware chunker that preserves BIS clause hierarchy rather than blind token cutting."""

    def __init__(self, max_chunk_words: int = 350, overlap_words: int = 40):
        self.max_chunk_words = max_chunk_words
        self.overlap_words = overlap_words

    def chunk_clauses(
        self,
        clauses: List[Dict[str, Any]],
        standard_metadata: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        chunks = []
        is_number = standard_metadata.get("is_number", "Unknown IS")
        title = standard_metadata.get("title", "")
        category = standard_metadata.get("category", "")
        industry = standard_metadata.get("industry", "")
        status = standard_metadata.get("status", "Active")

        chunk_idx = 0
        for item in clauses:
            clause_num = item.get("clause", "General")
            clause_title = item.get("title", "")
            section_num = item.get("section", "")
            page_num = item.get("page", 1)
            raw_content = item.get("content", "")

            # If clause content is within reasonable size, keep it as an atomic unit
            words = raw_content.split()
            if len(words) <= self.max_chunk_words:
                header = f"[{is_number} Clause {clause_num} - {clause_title}]" if clause_title else f"[{is_number} Clause {clause_num}]"
                full_text = f"{header}\n{raw_content}"
                chunks.append({
                    "chunk_index": chunk_idx,
                    "is_number": is_number,
                    "section": str(section_num),
                    "clause": str(clause_num),
                    "page": page_num,
                    "content": full_text,
                    "word_count": len(words),
                    "metadata": {
                        "is_number": is_number,
                        "standard_title": title,
                        "section": str(section_num),
                        "clause": str(clause_num),
                        "clause_title": clause_title,
                        "page": page_num,
                        "category": category,
                        "industry": industry,
                        "document_status": status,
                        "source": "BIS Official",
                    },
                })
                chunk_idx += 1
            else:
                # Sub-chunk with overlap while preserving the clause header on every piece
                start = 0
                sub_idx = 1
                while start < len(words):
                    end = min(start + self.max_chunk_words, len(words))
                    slice_words = words[start:end]
                    header = f"[{is_number} Clause {clause_num} - {clause_title} (Part {sub_idx})]"
                    full_text = f"{header}\n{' '.join(slice_words)}"
                    chunks.append({
                        "chunk_index": chunk_idx,
                        "is_number": is_number,
                        "section": str(section_num),
                        "clause": str(clause_num),
                        "page": page_num,
                        "content": full_text,
                        "word_count": len(slice_words),
                        "metadata": {
                            "is_number": is_number,
                            "standard_title": title,
                            "section": str(section_num),
                            "clause": str(clause_num),
                            "clause_title": clause_title,
                            "sub_part": sub_idx,
                            "page": page_num,
                            "category": category,
                            "industry": industry,
                            "document_status": status,
                            "source": "BIS Official",
                        },
                    })
                    chunk_idx += 1
                    sub_idx += 1
                    if end == len(words):
                        break
                    start += (self.max_chunk_words - self.overlap_words)

        return chunks
