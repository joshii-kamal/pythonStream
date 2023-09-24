from langchain.text_splitter import CharacterTextSplitter

class TextSplitter:
    def __init__(self, chunk_size=100, chunk_overlap=0):
        self.text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split_documents(self, data):
        return self.text_splitter.split_documents(data)
