import io
from typing import List, Dict, Any
import pypdf

class DocumentChunker:
    @staticmethod
    def extract_text(file_bytes: bytes, file_type: str) -> List[Dict[str, Any]]:
        """Extracts text and returns page/section items."""
        pages = []
        file_type = file_type.lower()

        if file_type == "pdf":
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append({"page_number": idx + 1, "text": text.strip()})
        else:
            # Plain text or markdown
            raw_text = file_bytes.decode("utf-8", errors="ignore")
            pages.append({"page_number": 1, "text": raw_text.strip()})

        return pages

    @staticmethod
    def split_text_with_overlap(
        pages: List[Dict[str, Any]],
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """Splits document text into chunks with defined overlap."""
        chunks = []
        chunk_idx = 0

        for p in pages:
            text = p["text"]
            page_num = p["page_number"]
            start = 0
            
            while start < len(text):
                end = min(start + chunk_size, len(text))
                chunk_text = text[start:end]
                chunks.append({
                    "chunk_index": chunk_idx,
                    "content": chunk_text,
                    "page_number": page_num
                })
                chunk_idx += 1
                if end == len(text):
                    break
                start += chunk_size - overlap

        return chunks
