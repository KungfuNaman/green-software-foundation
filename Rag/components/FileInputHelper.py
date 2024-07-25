import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from . import ImageExtractor
import pymupdf4llm


class FileInputHelper:

    def __init__(self, create_doc=True):
        self.create_doc = create_doc

    def load_documents(self, document_path, image_extract=True):
        """
            Load all PDFs in the DATA_PATH and convert them to markdown with images.
        """
        documents = []
        if self.create_doc:
            document = self.create_own_doc(document_path)
            documents.append(document)
        else:
            md_text = pymupdf4llm.to_markdown(document_path, write_images=True)
            if image_extract:
                ie = ImageExtractor('llava')
                md_text = ie.analyse_all_images_in_markdown(md_text)
            document = Document(page_content=md_text, metadata={"source": document_path})
            documents.append(document)

        return documents

    @staticmethod
    def create_own_doc(document_path: str):
        with open(document_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            document = Document(page_content=text_content, metadata={"source": document_path})
        return document

    @staticmethod
    def split_documents(documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)

    @staticmethod
    def calculate_chunk_ids(chunks):
        """
            This will create IDs like "data/monopoly.pdf:6:2"
            Page Source : Page Number : Chunk Index
        """
        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            source = FileInputHelper.dir_name_washing(source)
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks

    @staticmethod
    def load_json_file(path):
        with open(path, "r", encoding="utf-8") as file:
            file_data = json.load(file)
        return file_data

    @staticmethod
    def dir_name_washing(dir_str):
        dir_str = dir_str.replace("\\\\", "/")
        dir_str = dir_str.replace("\\", "/")
        return dir_str

