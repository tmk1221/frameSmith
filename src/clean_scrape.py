import re
from bs4 import BeautifulSoup as bs

# Uses beautifulsoup to remove unnecessary tags and classes from the scraped html
def extract_clean_text(input_html):
    soup = bs(input_html, 'html.parser')
    
    # Remove unnecessary tags
    for script in soup(['script', 'style', "nav", "noscript", "img", "button", "form", "input", "footer", "iframe", "head", "header", "aside"]):
        script.extract()
    
    # Remove unnecessary classes and IDs
    for elem in soup.select('.sidebar, #advertisements'):
        elem.extract()

    clean_text = soup.get_text()
    return clean_text

# Removes extra newlines and tabs from the text
def remove_extra_newlines_and_tabs(input_text):
    # Replace consecutive newlines and tabs with a single space
    clean_text = re.sub(r'[\n\t]+', ' ', input_text)

    return clean_text
