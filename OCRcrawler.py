import subprocess
import os
from pathlib import Path

import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory



def OCRcrawler(input_path):
    input_pdf_path = Path(input_path)
    output_pdf_path = os.path.join(os.path.dirname(input_pdf_path), "searchable_" + os.path.basename(input_pdf_path))

    tesseract_bin_path = "/opt/homebrew/bin"

    print(f"Attempting to convert '{input_pdf_path}' to a searchable PDF...")
    print(f"Output will be saved to: '{output_pdf_path}'")

    try:
        env = os.environ.copy()
        

        env["PATH"] = tesseract_bin_path + os.pathsep + env["PATH"]

        command = [
            'ocrmypdf',
            '--deskew',
            '--force-ocr',
            '--output-type', 'pdfa',
            input_pdf_path,
            output_pdf_path
        ]

        subprocess.run(
            command,
            check=True,  
            capture_output=True, 
            text=True, 
            env=env
        )
        print(f"Successfully converted '{input_pdf_path}' to searchable PDF: '{output_pdf_path}'")

    except subprocess.CalledProcessError as e:
        print(f"Error during OCR conversion:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        print("\nPossible reasons for failure:")
        print("  - Input PDF path is incorrect or file doesn't exist.")
        print("  - Tesseract OCR language data might be missing (e.g., eng.traineddata).")
    except FileNotFoundError:
        print("Error: 'ocrmypdf' command not found.")
        print("Please ensure ocrmypdf is installed and in your system's PATH.")
        print("You can install it using: pip install ocrmypdf")

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open the file dialog to select a file
    file_path = filedialog.askopenfilename(title='Select File') # Changed from askdirectory
    input_pdf = file_path
    input_path=input_pdf
    OCRcrawler(input_path)