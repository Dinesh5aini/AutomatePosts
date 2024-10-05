import os
import sys
import openai
from dotenv import load_dotenv
from exception import customException
from logger import logging

class PostGenerator:
    
    def __init__(self):
        try:
            load_dotenv()
            openai.api_key = os.getenv("OPENAI_API_KEY")

            logging.info("PostGenerator initialized successfully")
        
        except customException as e:
            logging.error("Error initializing PostGenerator", exc_info=True)
            raise customException(e, sys)

    def generate_post(topic, platform):
        try:
            system_message = f"""
            You are an expert content creator. Generate a detailed caption and image description for the following topic: {topic}.
            
            1. **Caption**: Write a long, informative caption (at least 100 words) that explains the key points of the topic and engages the audience. The caption should be educational and easy to understand.
            2. **Image Description**: Provide a description of the image that visually represents the topic with AI-related elements like icons, graphs, or abstract designs.

            Make sure the following are included:
            - Captions should clearly explain the topic, suitable for {platform}.
            - Image descriptions should align with the topic and have no text overlay.
            """

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Generate a detailed caption and image description for the topic: {topic}"}
                ]
            )

            logging.info("Post content generated successfully")

            return response.choices[0].message.content

        except customException as e:
            logging.error("Error generating post content", exc_info=True)
            raise customException(e, sys)
