from langchain.embeddings.openai import OpenAIEmbeddings

class Embeddings:
    def __init__(self, openai_api_key):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    def get_embeddings(self):
        return self.embeddings
