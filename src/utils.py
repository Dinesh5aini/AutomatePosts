import json 
import os
import sys
from logger import logging
from exception import customException

# parsing the strategy plan into a list of topics
def parse_strategy_plan(strategy_plan):
    try:

        print("Parsing strategy plan...")
        
        topics = []
        for line in strategy_plan.split("\n"):
            if line.startswith("Topic:"):
                topics.append(line.replace("Topic: ", "").strip())

        logging.info("Strategy plan parsed successfully")

        return topics
    
    except customException as e:
        logging.error("Error parsing strategy plan", exc_info=True)
        raise customException(e, sys)


# saving the post plan to a JSON file
def save_post_plan(posts, output_dir, output_file_name):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file=os.path.join(output_dir, output_file_name)

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(posts, file, ensure_ascii=False, indent=4)
        print(f"Post plan saved to {output_file}.")

        logging.info("Post plan saved successfully")

    except customException as e:
        logging.error("Error saving post plan", exc_info=True)
        raise customException(e, sys)