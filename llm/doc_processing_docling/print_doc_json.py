from docling.document_converter import DocumentConverter
import json
source = "/home/ankdesh/temp/sample.pdf"  # document per local path or URL
converter = DocumentConverter()
doc = converter.convert(source).document
with open("doc.json","w", encoding="utf-8") as fp:
    fp.write(json.dumps(doc.export_to_dict()))
