import sys

from langchain_community.document_loaders import PyMuPDFLoader
import pymupdf4llm
import os
import pathlib


def extractText(pdfPath):
    loader = PyMuPDFLoader(pdfPath)
    data = loader.load()
    with open("./extractText", "w", encoding="utf-8") as file:
        for page in data:
            file.write(page.page_content)
            file.write("\n\n")


def extractWithImages(pdf_path, output_dir):

    md_text = pymupdf4llm.to_markdown(pdf_path, write_images=True)

    # output_dir = "./documentExtraction/outputs/extractWithImages.md"

    pathlib.Path(output_dir).write_bytes(md_text.encode())

    # with open(output_dir, "w", encoding="utf-8") as file:
    #     # Write the markdown text to the file
    #     file.write(md_text)
    #     file.write("\n\n")


if __name__ == "__main__":
    pdf_path = r"E:\PROJECTS\Python_Projects\gsf_docextraction\green-software-foundation\documentsFromText\Netflix\Netflix_Document.pdf"
    output_dir = r"E:\PROJECTS\Python_Projects\gsf_docextraction\green-software-foundation\documentsFromText\Netflix\Netflix_Document.md"
    extractWithImages(pdf_path, output_dir)
