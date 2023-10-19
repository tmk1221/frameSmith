from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import AsyncChromiumLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
import csv
from clean_scrape import extract_clean_text, remove_extra_newlines_and_tabs

# Generates a Lean Canvas
def lean_canvas(product, openai_model, news_urls, youtube_urls=None):
    
   # Load in News
    loader = AsyncChromiumLoader(news_urls)
    docs = loader.load()

    # Remove extra HTML tags from articles
    for doc in docs:
        cleaned_text = extract_clean_text(doc.page_content)
        cleaned_text = remove_extra_newlines_and_tabs(cleaned_text)
        doc.page_content = cleaned_text

    # Load in YouTube videos
    if youtube_urls is not None:
        for video_url in youtube_urls:
            loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=True)
            youtube = loader.load()
            if youtube == []:
                "Transcript not available for video: " + video_url
            else:
                docs.append(youtube[0])

    #Print cleaned texts to ensure they were scraped and cleaned properly
    #print(docs)

    print("Data sour loaded")

    # Split documents into 1000 character chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    texts = splitter.split_documents(docs)

    print("Splitting articles into 1000 character chunks")

    # Embed each document chunk for search/retrieval
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    docsearch = Chroma.from_documents(texts, embeddings)

    print("Embedding each article chunk for later search and retrieval")

    # Setup chains
    llm = ChatOpenAI(temperature=0, model=openai_model)

    template = """You are a research chatbot having a conversation with a human.

    Given the following information about {product}, give a professional and detailed answer to the final question.
    
    {context}

    {chat_history}
    Human: {human_input}
    Chatbot:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input", "context"], template=template, partial_variables={"product": product}
    )
    memory = ConversationBufferWindowMemory(k=1, memory_key="chat_history", input_key="human_input")
    chain = load_qa_chain(
        llm, chain_type="stuff", memory=memory, prompt=prompt
    )
    
    # Lean Canvas Questions
    queries = {
    "overall": f"What is {product}? Give a description of what it does and why it exists.",
    "target_users": f"Who is {product} intended for? These groups of people are called target users. Target users are people who have either already adopted {product}, or who {product} is intended for. If this information wasn't provided, list some plausible target users of {product}.",
    "problems": f"What are the reasons for target users to seek out, and adopt, {product}? These reasons are usually problems or pain points the target users are experiencing. Reasons can also be the needs and desires of target users. If this information wasn't provided, list some plausible reasons for target users to seek out and adopt {product}. You don't need to explain how {product} addresses these reasons yet, that will come next.",
    "solutions": f"How does {product} address each one of these reasons? In other words, how does {product} solve user problems, assuage user pain points, or fulfill user needs and desires? If this information wasn't provided, list the plausible ways {product} could address each one of these reasons.",
    "unfair_advantage": f"What makes {product} difficult to compete with? These are {product}'s competitive advantages, or the barriers to entry faced by its competitors. If this information wasn't provided, list some plausible competitive advantages and barriers to entry.",
    "unique_value_proposition": f"What makes {product} unique or special compared to others? This should be a 2-3 sentence unique value proposition.",
    "channels": f"Which channels does {product} use to reach its target users? Channels include where {product} is marketed to its potential users and where users access {product} (e.g. mobile app, website, etc.). If this information wasn't provided, list some plausible channels for {product}.",
    "costs": f"What operating costs are incurred by {product} during development, launch, and maintainance. If this information wasn't provided, list some plausible operating costs.",
    "revenue": f"How does {product} generate revenue? Give a description of plausible business models and revenue streams for {product}."
    }

    # Generate Lean Canvas
    results = {}
    for key, query in queries.items():
        docs = docsearch.similarity_search(query)
        result = chain({"input_documents": docs, "human_input": query}, return_only_outputs=True)

        results[key] = result
        print(f"✅ {key.replace('_', ' ').capitalize()}")

    # Write to CSV
    filename = f"./lean_canvas_output/{product}_lean_canvas.csv"

    print("Writing to filename: ", filename)

    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Section", "Details"])
        for key, value in results.items():
            csv_writer.writerow([key.replace('_', ' ').capitalize(), value])