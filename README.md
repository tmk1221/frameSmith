# Lean Canvas Bot 3000
This bot scrapes information from the web and YouTube videos, and uses an OpenAI LLM to generate a Lean Canvas based on said information.

## Installation
1. Clone this repository
```
gh repo clone tmk1221/lean_canvas_bot
cd lean_canvas_bot
```

2. Create virtual environment, and install Python dependencies.
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a file in the root directory called `.env`, and add your OpenAI API as shown below.

4. Change the following variables in the config.json file
    1. `product`: Use the product/company name that is used in the sources you provide.

    2. `openai_model`: The OpenAI model used to generate the Lean Canvas.

    - Note: At the time of writing, the most common options are: "gpt-3.5-turbo" or "gpt-4". GPT-4 is a more powerful model, but will cost more to use. For up-to-date information about available models, see [OpenAI's Model Overview](https://platform.openai.com/docs/models/overview)

    3. `news_urls`: Websites, blog posts and/or news articles specific to your product/company.

    - Note 1: You need to provide at least 1 URL here for the bot to run.

    - Note 2: BeautifulSoup is used to scrape text from these websites. The text then goes through a cleaning step. You may want to print the texts afterwards to ensure that the texts were scraped and cleaned in the way you expected. See line 36 in `src/lean_canvas_generator.py` for what I mean.

    4. `youtube_urls`: YouTube videos specific to your product/company.

    - Note 1: You do not need to provide any YouTube videos for the bot to run. If you do not want to use any YouTube videos, then replace the brackets with `None` in the config.json file.

    - Note 2: Transcript texts are captured via YouTube's API. Some YouTube videos don't have transcripts. If this is the case, it's okay, the API will just return an empty string.

5. Run the bot
```
python3 ./src/generate.py
```

6. Lean Canvas output can be found in `./lean_canvas_output`