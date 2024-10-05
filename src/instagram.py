import os
import sys
import time
import schedule
import requests
from logger import logging
from dotenv import load_dotenv
from exception import customException
from datetime import datetime, timedelta
from image_generator import ImageGenerator


class InstagramPost:
    def __init__(self):
        try:
            load_dotenv()
            self.user_access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
            self.fb_page_id = os.getenv('FACEBOOK_PAGE_ID')
            self.posts_queue = []
            logging.info("InstagramPostScheduler initialized successfully")
        except customException as e:
            logging.error("Error initializing InstagramPostScheduler", exc_info=True)
            raise customException(e, sys)

    def get_page_access_token(self):
        try:
            url = f"https://graph.facebook.com/v20.0/{self.fb_page_id}?fields=instagram_business_account&access_token={self.user_access_token}"
            response = requests.get(url)
            data = response.json()
            if data and "instagram_business_account" in data:
                ig_user_id = data["instagram_business_account"]["id"]
                page_access_token = self.user_access_token  
                return page_access_token, ig_user_id
            else:
                logging.error("No linked Instagram business account found.")
                return None, None
            
        except customException as e:
            logging.error("Error fetching page access token", exc_info=True)
            raise customException(e, sys)

    def upload_media(self, ig_user_id, image_url, caption, page_access_token):
        try:
            url = f"https://graph.facebook.com/v20.0/{ig_user_id}/media"
            params = {
                "caption": caption,
                "access_token": page_access_token,
                "image_url": image_url
            }
            response = requests.post(url, params=params)
            data = response.json()
            if "id" in data:
                return data["id"]  # IG Container ID
            else:
                logging.error(f"Error uploading media: {data}")
                return None
            
        except customException as e:
            logging.error("Error uploading media", exc_info=True)
            raise customException(e, sys)

    def publish_post(self, ig_user_id, ig_container_id, page_access_token):
        try:
            publish_url = f"https://graph.facebook.com/v20.0/{ig_user_id}/media_publish"
            publish_params = {
                "creation_id": ig_container_id,
                "access_token": page_access_token
            }
            print("Publishing post...")
            publish_response = requests.post(publish_url, params=publish_params)
            data = publish_response.json()
            if "id" in data:
                logging.info(f"Post published successfully: {data['id']}")
                print("Post published successfully.")
            else:
                logging.error(f"Error publishing post: {data}")
        except customException as e:
            logging.error("Error publishing post", exc_info=True)
            raise customException(e, sys)

    def add_post_to_queue(self, img_description, caption):
        self.posts_queue.append({"img_description": img_description, "caption": caption})

    # def schedule_posts(self):
    #     if not self.posts_queue:
    #         logging.warning("No posts in the queue to schedule.")
    #         return
    #     page_access_token, ig_user_id = self.get_page_access_token()
    #     if not page_access_token or not ig_user_id:
    #         logging.error("Failed to get page access token or Instagram user ID.")
    #         return
    #     for i, post in enumerate(self.posts_queue):
    #         image_name = rf"artifacts\images\image_{i+1}.jpg"
    #         schedule_time = datetime.now() + timedelta(minutes=i+1)  # Schedule 1 minute apart, starting 1 minute from now
    #         schedule.every().day.at(schedule_time.strftime("%H:%M")).do(
    #             self.post_to_instagram,
    #             ig_user_id=ig_user_id,
    #             img_description=post["img_description"],
    #             caption=post["caption"],
    #             page_access_token=page_access_token,
    #             image_name=image_name
    #         )
    #         logging.info(f"Scheduled post for {schedule_time}")


    def schedule_posts(self, post_time):
        if not self.posts_queue:
            logging.warning("No posts in the queue to schedule.")
            return

        page_access_token, ig_user_id = self.get_page_access_token()
        if not page_access_token or not ig_user_id:
            logging.error("Failed to get page access token or Instagram user ID.")
            return

        for i, post in enumerate(self.posts_queue):
            image_name = rf"artifacts\images\image_{i+1}.jpg"

            # Schedule one post per day at the specific time provided by the user
            schedule.every().day.at(post_time).do(
                self.post_to_instagram,
                ig_user_id=ig_user_id,
                img_description=post["img_description"],
                caption=post["caption"],
                page_access_token=page_access_token,
                image_name=image_name
            )


    def post_to_instagram(self, ig_user_id, img_description, caption, page_access_token, image_name):
        try:
            # Generate image URL just before posting
            image_url = ImageGenerator.generate_image(img_description)
            
            ig_container_id = self.upload_media(ig_user_id, image_url, caption, page_access_token)
            if ig_container_id:
                self.publish_post(ig_user_id, ig_container_id, page_access_token)
                with open(image_name, 'wb') as f:
                    f.write(requests.get(image_url).content)
            else:
                logging.error("Failed to upload media.")
        except Exception as e:
            logging.error(f"Error posting to Instagram: {str(e)}")

    def run_scheduler(self):
        while len(self.posts_queue) > 0: 
            schedule.run_pending()  # Run scheduled tasks
            time.sleep(60)  # Check every minute

        logging.info("All posts have been processed, exiting scheduler.")
        exit()

    @staticmethod
    def instagram_main(posts, post_time):
        scheduler = InstagramPost()
        for post in posts:
            scheduler.add_post_to_queue(post['img_description'], post['caption'])
        logging.info(f"Added {len(posts)} posts to the queue.")
        # Schedule the posts
        scheduler.schedule_posts(post_time)
        # Run the scheduler
        scheduler.run_scheduler()