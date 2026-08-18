# document-parser

استخراج متن تمیز از اسناد دانش برای pipeline RAG پلتفرم MousaviTax.

برگرفته از `MKA-Core/packages/document-parser` (ADR-003).

## فرمت‌های پشتیبانی‌شده

- PDF (متنی) — `pdfplumber` + fallback با `pypdf`
- DOCX — `python-docx`
- Markdown / plain text

## استفاده

```bash
cd packages/document-parser
pip install -r requirements.txt

# تست CLI
python -m app.cli /path/to/قانون.pdf --json --chunks
```

```python
from app.parser import DocumentParser

parser = DocumentParser(chunk_size=1200, chunk_overlap=200)
doc = parser.parse_file("قانون مالیاتهای مستقیم.pdf")
assert doc.success
for chunk in doc.chunks:
    print(chunk.page, chunk.text[:80])
```

## خروجی

`ParsedDocument` شامل:
- `full_text`
- `chunks` (آماده embedding / retrieval)
- `page_count`, `metadata`, `error`

خروجی chunkها با مدل `DocumentChunk` در `packages/shared` هم‌راستا است (پس از تبدیل در knowledge-core).

## وضعیت

منتقل‌شده از MKA-Core — آماده اتصال به knowledge-core.
