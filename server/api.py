from ocrprocessor import OCRProcessor

with open("data/test_ocr.md") as f:
    ocr_markdown = f.read()

ocr = OCRProcessor(ocr_markdown)

# print(ocr.ocr_markdown)
# ocr.process_chunks()

# print(ocr.detect_phrases(ocr.process_chunks()))
ocr.convert_units(ocr.detect_phrases(ocr.process_chunks()))