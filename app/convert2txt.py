import regex as re
import argparse
import os
from docling.document_converter import DocumentConverter

def convert_pdf_to_text(source_path):
    # PDF를 텍스트로 변환
    converter = DocumentConverter()
    result = converter.convert(source_path)
    text = result.document.export_to_text()

    # 정규표현식을 사용하여 HTML 주석 제거
    text = re.sub(r'<!--.*?-->', '', text)

    # 페이지 숫자 제거 (예: [Page 1], [1], 1 등)
    text = re.sub(r'\[Page \d+\]|\[\d+\]|\b\d+\b(?=\s*$)', '', text)

    # 읽을 수 없는 특수 기호 제거 (유니코드 문장 부호는 유지)
    # text = re.sub(r'[^\w\s\p{P}]', '', text, flags=re.UNICODE)

    # 연속된 공백 제거 및 앞뒤 공백 제거
    # text = re.sub(r'\s+', ' ', text).strip()

    return text

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert PDF to text file"
    )
    parser.add_argument("--input", "-i", help="Path to the input PDF file")
    parser.add_argument(
        "--output",
        "-o",
        default=".",
        help="Output folder for the text file (default: current directory)",
    )
    parser.add_argument(
        "--filename",
        "-n",
        default="converted_text",
        help="Output text filename without extension (default: converted_text)",
    )
    args: argparse.Namespace = parser.parse_args()

    # PDF를 텍스트로 변환
    cleaned_text = convert_pdf_to_text(args.input)

    # 출력 파일 경로 생성
    output_path = os.path.join(args.output, f"{args.filename}.txt")

    # 텍스트를 파일로 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Converted text saved to: {output_path}")

if __name__ == "__main__":
    main()

