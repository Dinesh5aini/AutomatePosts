# AutomatePosts

AutomatePosts is a project designed to automate the generation and scheduling of social media posts for platforms like Instagram, Facebook, and Twitter using OpenAI's GPT-4 and DALL·E models.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Setup Instructions

### 1. Meta for Developers
1. Go to [Meta for Developers](https://developers.facebook.com/).
2. Create a new app.

### 2. Graph API Explorer
1. Go to the [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. Get a user access token with the following permissions:
    - `pages_show_list`
    - `ads_management`
    - `business_management`
    - `instagram_basic`
    - `instagram_manage_comments`
    - `instagram_manage_insights`
    - `instagram_content_publish`
    - `pages_read_engagement`

### 3. Environment Variables
1. Add the user access token to the `.env` file:
    ```env
    INSTAGRAM_ACCESS_TOKEN=your_user_access_token_here
    ```

2. Get the Facebook Page ID for the page connected with the user access token. You can find the page access token in the page's "About" section under "Page Transparency".
3. Add the Facebook Page ID to the `.env` file:
    ```env
    FACEBOOK_PAGE_ID=your_facebook_page_id_here
    ```

4. Add your OpenAI API key to the `.env` file:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

### 4. Virtual Environment and Dependencies
1. Create a virtual environment:
    ```sh
    python -m venv apenv
    ```

2. Activate the virtual environment:
    - On Windows:
        ```sh
        apenv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source apenv/bin/activate
        ```

3. Install the dependencies by running [setup.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22c%3A%5C%5CUsers%5C%5Cdines%5C%5COneDrive%5C%5CDesktop%5C%5CBTH%20internship%5C%5CProjects%5C%5CAutomatePosts%5C%5Csetup.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FUsers%2Fdines%2FOneDrive%2FDesktop%2FBTH%20internship%2FProjects%2FAutomatePosts%2Fsetup.py%22%2C%22scheme%22%3A%22file%22%7D%7D):
    ```sh
    python setup.py install
    ```

## Usage

1. **Run the Main Script:**
   - Execute the main script to generate and schedule posts:
    ```sh
    python src/main.py
    ```

2. **Input the Required Values:**
   - Domain (e.g., 'Technology', 'Finance')
   - Platform (e.g., 'Instagram', 'LinkedIn', 'Twitter')
   - Theme (e.g., 'AI & ML', 'Business Automation', 'Data Science')
   - Summary of the post content
   - Number of days for the post plan
   - Time to post the content in HH:MM format (e.g., 15:30 for 3:30 PM)

## Project Structure

```plaintext
AutomatePosts/
├── artifacts/
│   ├── images/                       # Generated images will be stored here
│   └── post_plan.json                # Generated post plan
│   
├── src/
│   ├── __pycache__/                  # Compiled Python files
│   ├── exception.py                  # Custom exceptions for error handling
│   ├── facebook.py                   # Module for Facebook API interactions
│   ├── image_generator.py            # Module for generating images
│   ├── instagram.py                  # Module for Instagram API interactions
│   ├── logger.py                     # Configures logging for the application
│   ├── main.py                       # Main script to run the application
│   ├── post_generator.py             # Module for generating post content
│   ├── strategy_generator.py         # Module for generating content strategy plans
│   ├── twitter.py                    # Module for Twitter API interactions
│   └── utils.py                      # Utility functions for parsing and saving data
│   
├── .env                              # Environment variables, such as API keys
├── requirements.txt                  # Python dependencies
├── setup.py                          # Script for setting up the package
├── .gitignore                        # Git ignore file to exclude certain files and directories
└── README.md                         # Project documentation