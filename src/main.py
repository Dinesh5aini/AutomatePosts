import sys
import re
from logger import logging
from exception import customException
from strategy_generator import StrategyGenerator
from post_generator import PostGenerator
from instagram import InstagramPost
from utils import parse_strategy_plan, save_post_plan

# function for generating a strategy plan
def generate_post_plan(post_plan_generator : StrategyGenerator, days: int):
    try:
        # Generate strategy plan
        strategy_plan = post_plan_generator.generate_strategy_plan(days)

        # Parse the strategy plan into a list of topics
        topics = parse_strategy_plan(strategy_plan)

        # Generate posts for each topic
        posts = []
        for day, topic in enumerate(topics, start=1):
            print(f"Generating post for Day {day}: {topic}")
            post = PostGenerator.generate_post(topic=topic, platform=post_plan_generator.platform)

            posts.append({
                "day": day,
                "topic": topic,
                "caption" : re.sub(r"\*\*.*?\*\*\s*:?\s*", "", post.split("\n\n")[0]),
                "img_description" : re.sub(r"\*\*.*?\*\*\s*:?\s*", "", post.split("\n\n")[1])
            })

        logging.info("Post plan generated successfully")
        
        return posts
    
    except customException as e:
        logging.error("Error generating post plan", exc_info=True)
        raise customException(e, sys)


def main():
    try:
        # Get user input for domain, platform, theme, summary, and days
        domain = input("Enter domain (e.g., 'Technology', 'Finance'): ")
        platform = input("Choose platform [Instagram, LinkedIn, Twitter]: ")
        theme = input("Choose theme [AI & ML, Business Automation, Data Science]: ")
        summary = input("Enter a brief summary of the post content: ")
        days = int(input("Enter the number of days for the post plan: "))
        post_time = input("Enter the time to post the content in HH:MM format (eg. 15:30 for 3:30 PM): ")

        # Initialize PostPlanGenerator
        post_plan_generator = StrategyGenerator(domain, platform, theme, summary)

        # Generate the strategy plan and posts
        posts = generate_post_plan(days=days, post_plan_generator=post_plan_generator)

        
        posts_output_dir = "artifacts"
        output_file_name = "post_plan.json"

        # Save the plan to a file
        save_post_plan(posts=posts, output_dir=posts_output_dir, output_file_name=output_file_name)

        # Publish the AI generated posts on Instagram
        instagram = InstagramPost()
        InstagramPost.instagram_main(posts= posts, post_time=post_time)


    except customException as e:
        logging.error("Error in main function", exc_info=True)
        raise customException(e, sys)
    

if __name__ == "__main__":
    main()