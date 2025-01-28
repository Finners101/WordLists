#pip install PyPDF2
import PyPDF2

def extract_pdf_to_text(pdf_path, output_text_file):
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            with open(output_text_file, 'w', encoding='utf-8') as text_file:
                # Loop through each page and extract text
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:  # Check if the page contains text
                        for line in text.split('\n'):
                            line=line.strip()
                            if len(line):
                                text_file.write(line+"\n")
        print(f"Text successfully extracted to {output_text_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_file(file_path, of):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, start=1):
                # Strip leading/trailing whitespace
                line = line.strip()

                # Skip empty lines or lines with a single character
                if len(line) <= 1:
                    continue

                # Skip lines ending with "Preliminary and Preliminary for Schools"
                if line.startswith("© Cambridge University Press"):
                    continue

                # Skip lines starting with "•"
                if line.startswith("•"):
                    continue

                if line.startswith("B1 Preliminary "):
                    continue

                # Warn about lines that don't end with text in parentheses
                if not line.endswith(")") or "(" not in line:
                    print(f"Warning: Line {line_num} does not end with text in parentheses: {line}")

                # Warn about lines starting with text in parentheses
                if line.startswith("("):
                    print(f"Warning: Line {line_num} starts with text in parentheses: {line}")

                # Process the line (if needed)
                of.write(line+"\n")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


#PDF
pdf_path = "flyers-word-list.pdf"  # Replace with your PDF file path
output_text_file = "flyers-word-list.txt"  # Replace with your desired output text file name
extract_pdf_to_text(pdf_path, output_text_file)

'''
file_path = "Cambridge_Perliminary_2020.txt"  # Replace with your file path
outfile = "Cambridge_Perliminary_2020_cl.txt"
with open(outfile, "w") as of:
    process_file(file_path, of)
'''