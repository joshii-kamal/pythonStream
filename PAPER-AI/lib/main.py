import sys

sys.path.append('../')

from config.get_config import get_config
from lib.csv_loader import DataLoader
from lib.text_splitter import TextSplitter
from lib.embeddings import Embeddings
from lib.vectorstores import VectorStore
from lib.open_ai import AskOpenAI


def main(user_question, user_ans):
    config = get_config()
    data_loader = DataLoader(file_path="data/subject.csv")
    data = data_loader.load_data()

    text_splitter = TextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(data)

    embed_instance = Embeddings(openai_api_key=config['apiKey'])
    embeddings = embed_instance.get_embeddings()
    db = VectorStore.from_documents(docs, embeddings)
    db.save_local('./vectors/')

    response = db.similarity_search(user_question)
    system_answer = response[0].page_content if len(response) > 0 else None

    prompt_start = "Compare given answers given by Professor (A) and Student (B), and calculate the score of the " \
                   "student (B) answer."
    prompt_end = "Note: Calculate score like 8/10, it should be between 0 to 10. If you don't understand answer " \
                 "provided by student give lowest score. But response format must be like: 8/10"
    prompt = f"{prompt_start}\n\nA. {system_answer}\n\nB. {user_ans}\n\n{prompt_end}"

    ai_response = AskOpenAI().ask(prompt)

    return ai_response
