import os
import sys
import openai
from logger import logging
from dotenv import load_dotenv
from exception import customException


class ImageGenerator:

    def __init__(self):
        try:
            load_dotenv()

            openai.api_key = os.getenv("OPENAI_API_KEY")

            logging.info("ImageGenerator initialized successfully")

        except customException as e:
            logging.error("Error initializing ImageGenerator", exc_info=True)
            raise customException(e, sys)

    def generate_image(prompt, size="1024x1024"):
        try:

            print("Generating image from prompt: ", prompt)

            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                n=1,
            )
            
            image_url = response.data[0].url

            logging.info(f"Generated image from prompt: {prompt} using OpenAI")
            
            return image_url

        except Exception as e:
            logging.error("Error in imageGenerator.generate_with_openai", exc_info=True)
            raise customException(e, sys)