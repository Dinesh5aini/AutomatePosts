import os
import sys
import openai
from dotenv import load_dotenv
from logger import logging
from exception import customException

class StrategyGenerator:
    
    def __init__(self, domain, platform, theme="AI & ML", summary="generate by yourself"):
        try:
            load_dotenv()  # Load OpenAI API key from environment variables
            openai.api_key = os.getenv("OPENAI_API_KEY")

            self.domain = domain
            self.platform = platform
            self.theme = theme
            self.summary = summary

            logging.info("StrategyGenerator initialized successfully")

        except customException as e:
            logging.error("Error initializing StrategyGenerator", exc_info=True)
            raise customException(e, sys)

    def generate_strategy_plan(self, days):
        try:
            print(f"Generating {days}-day content strategy plan for {self.theme} in the {self.domain} domain on {self.platform}...")

            system_message = f"""
            You are an expert content strategist. Create a {days}-day content strategy plan for {self.theme} in the {self.domain} domain on {self.platform}.
            The plan should provide a unique topic for each day that aligns with the overall theme and keeps the audience engaged.
            
            Ensure the following:
            1. Each topic should be distinct and relevant to {self.theme}.
            2. The topics should cover a wide range of aspects, focusing on educating the audience.
            3. Ensure the content is spread out evenly across the {days}-day period and avoids repetition.
            
            Format the output as follows:
            
            Day 1:
            Topic: [Brief topic]
            
            Day 2:
            Topic: [Brief topic]
            
            Continue this format for all and exact {days} days.

            Note: There is no need to provide detailed content for each topic, just a brief topic idea.
            """

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Create a {days}-day content strategy plan based on the following summary:\n\n{self.summary}"}
                ]
            )

            logging.info("Strategy plan generated successfully")

            return response.choices[0].message.content
        
        except customException as e:
            logging.error("Error generating strategy plan", exc_info=True)
            raise customException(e, sys)
        