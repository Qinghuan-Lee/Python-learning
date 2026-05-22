import pdfplumber
from deep_translator import GoogleTranslator

pdf_path = "Probability - for the enthusiastic beginner -- David J. Morin -- ( WeLib.org ).pdf"
output_file = "ans.txt"

translator = GoogleTranslator(source='en', target='zh-CN')

with pdfplumber.open(pdf_path) as pdf:
    with open(output_file, "w", encoding="utf-8") as f:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                translated = translator.translate(text)
                f.write(translated + "\n\n")

print("翻译完成")