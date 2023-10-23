import time
import dotenv
import json
from framework_generator import framer

# Record start time
start_time = time.time()

# Load in OpenAI API Key from .env
dotenv.load_dotenv()

# Load in config variables from config.json
with open('./config.json') as config_file:
    config = json.load(config_file)
product = config["product"]
openai_model = config["openai_model"]
news_urls = config["news_urls"]
youtube_urls = config["youtube_urls"]
framework_questions = config["framework_questions"]

framework_questions_formatted = {key: value.format(product=product) for key, value in framework_questions.items()}

framer(product, framework_questions_formatted, openai_model, news_urls, youtube_urls)

# Record end time
end_time = time.time()

# Calculate elapsed time
execution_time = end_time - start_time

print(f"Execution time: {execution_time:.2f} seconds")