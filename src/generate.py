import time
import dotenv
import json
from lean_canvas_generator import lean_canvas

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

lean_canvas(product, openai_model, news_urls, youtube_urls)

# Record end time
end_time = time.time()

# Calculate elapsed time
execution_time = end_time - start_time

print(f"Execution time: {execution_time:.2f} seconds")