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


def extractWithImages(pdfPath):

    md_text = pymupdf4llm.to_markdown(pdfPath, write_images=True)

    output_dir = "./documentExtraction/outputs/extractWithImages.txt"

    pathlib.Path("./documentExtraction/outputs/extractWithImages.md").write_bytes(md_text.encode())

    # with open(output_dir, "w", encoding="utf-8") as file:
    #     # Write the markdown text to the file
    #     file.write(md_text)
    #     file.write("\n\n")


# extractTextUsingLangChain("./documents/2.pdf")
extractWithImages("./documents/3.pdf")
