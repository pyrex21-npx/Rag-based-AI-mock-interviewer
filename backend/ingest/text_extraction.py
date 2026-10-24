from pypdf import PdfReader
from io import BytesIO

LIGATURES = {
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
    "\ufb03": "ffi", "\ufb04": "ffl",
}

def sanitize_text(text):
    text = text.replace("\x00" , "")
    for lig , replacement in LIGATURES.items():
        text = text.replace(lig , replacement)
    return text    
def extract_text_from_file(path): 
    text_parts = []
    blank_parts = []
    reader = PdfReader(path)
    for pageno, text in enumerate(reader.pages):
        extracted = text.extract_text()
        if not extracted:
            blank_parts.append(pageno)
        else:
            text_parts.append(sanitize_text(extracted))    
    print(blank_parts)
    return "".join(text_parts)

