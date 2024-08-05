import base64
import requests
import json
import re


class ImageExtractor:
    def __init__(self, model_name):
        self.model_name = model_name
        self.prompt = 'Summarise the given image. If the image is a software architecture diagram describe all the key components in your summary.'

    def __encode_image_to_base64(self, image_path):
        with open(image_path, 'rb') as image_file:
            image_binary = image_file.read()
            # Encode the image to base64
            encoded_image = base64.b64encode(image_binary).decode('utf-8')
            return encoded_image

    def __query_local(self, image_path):
        encoded_image = self.__encode_image_to_base64(image_path)
        api_url = 'http://localhost:11434/api/generate'
        payload = {
            "model": self.model_name,
            "prompt": self.prompt,
            "stream": False,
            "images": [encoded_image]
        }
    
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(api_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status() 
            return response.json()  
        except Exception as e:
            print(e)

    def analyse_all_images_in_markdown_file(self, markdown_path):
        with open(markdown_path, 'r', encoding="utf-8") as file:
            markdown_content = file.read()
    
        markdown_content = self.analyse_all_images_in_markdown(markdown_content)

        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def analyse_all_images_in_markdown(self, markdown_content):
        print("Extracting Images from Document..")
        image_pattern = r'!\[(.*?)\]\((.*?)\)'
        matches = re.findall(image_pattern, markdown_content)
        no = 0
        for match in matches:
            image_alt = match[0]
            image_path = match[1]
            if(image_path.startswith("http")):
                continue
            response = self.__query_local(image_path)
            text_response = response['response']
            no += 1
            markdown_content = markdown_content.replace(f"![{image_alt}]({image_path})", f"Image {no}: {text_response}")
        print("Image Extraction Complete!")
        return markdown_content
    
#ie = ImageExtractor("llava")
#ie.analyse_all_images_in_markdown_file("documentExtraction/outputs/extractWithImages.md")
