import PyPDF2
import argparse

def pdf_to_txt(pdf_path, txt_path):
    # PDF 파일 객체 생성
    with open(pdf_path + ".txt", 'rb') as pdf_file:
        # PDF 리더 객체 생성
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # 텍스트 추출
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # 추출된 텍스트를 TXT 파일로 저장
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to TXT')
    parser.add_argument('--input', "-i", help='Input PDF file path')
    parser.add_argument('--output', "-o", help='Output TXT file path')
    args = parser.parse_args()

    pdf_to_txt(args.input, args.output)
    print(f"### Converted {args.input} to {args.output} ###")

if __name__ == "__main__":
    main()
