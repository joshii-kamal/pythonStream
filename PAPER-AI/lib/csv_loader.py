
from langchain.document_loaders.csv_loader import CSVLoader
class DataLoader:
    def __init__(self, file_path):
        self.loader = CSVLoader(
            file_path=file_path,
            csv_args={
                "delimiter": ",",
                "fieldnames": ["question", "answer"],
            },
            encoding='utf-8',
        )

    def load_data(self):
        return self.loader.load()
