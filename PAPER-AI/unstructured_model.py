import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI, OpenAIChat
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
import openai
from config.get_config import get_config

config = get_config()
api_key = config['apiKey']
model = config['model']


# Initialize the question-answering chain

def get_question_score(q, ans):
    # os.environ["OPENAI_API_KEY"] = config['apiKey']
    os.environ["OPENAI_API_KEY"] = api_key

    loader = DirectoryLoader('./sources/', glob="./*.txt")
    documents = loader.load()

    # Splitting the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Using OpenAI embeddings (can be swapped to local embeddings in the future)
    embedding = OpenAIEmbeddings()

    vectordb = FAISS.from_documents(documents=texts, embedding=embedding)

    # Loading the persisted database from disk
    retriever = vectordb.as_retriever()

    llm = OpenAI()

    # Creating the chain to answer questions
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True)

    # Define the prompt for scoring
    prompt_start = "Compare answers given by Professor (A) and Student (B)."
    prompt_end = """
    Calculate score for the Student's (B) answer.\n
    If the student's answer is not correct then don't hesitate to give a low score.\n
    Note: Response json format: {'score': '5/10', 'reason': 'your reason upto to 2 lines'}.
    Also not to responed in any other format other then mentioned on the Note"""
    prompt_question = f"Question: {q}"

    system_answer = qa_chain(q)

    # print(system_answer)

    final_prompt = f"{prompt_start}\n\n{prompt_question}\n\nA. {system_answer}\n\nB. {ans}\n\n{prompt_end}"

    # Use OpenAI API to get a response based on the prompt
    ai_response = openai.ChatCompletion.create(
        model=model,
        # model=config['model'],
        messages=[
            {"role": "system", "content": "You are a professor"},
            {"role": "user", "content": final_prompt},
        ],
        max_tokens=1000,
        api_key=api_key,
    )

    # Extract the response from the AI model and return it as the score
    return ai_response.choices[0].message.content


def gpt_res(file_contents):
    # Create a prompt for ChatGPT to process the file content
    # print("file_contents inside gpt", file_contents)
    prompt = f"""
     YOUR EXPERTIES: 
        1- You are an expert in parsing the file content. 
    
    DATA : {file_contents}
    
    JSON_FORMAT : {{
        "question" : " ",
        "answer" : " "
      }}
     TASK:
        1- understand the given DATA.
        2- extract the question and answer accordingly
        3- store it in a json object
        
     INSTRUCTION : 
        1- Return the question and answer in JSON_FORMAT and it should be json object.
        2- Do not return any additional text along with the JSON_FORMAT object 
        3- Do not add any additional characters
        4- Do not add any new line
    """

    # print("prompt:::::::::::::<><>", prompt)
    # Send the prompt to ChatGPT and obtain a response
    ai_response = openai.ChatCompletion.create(
        model=model,
        # model=config['model'],
        messages=[
            {"role": "system", "content": "You are a data extractor"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        api_key=api_key,

    )

    # Extract the JSON response from the AI model
    # print("ai_response::::::::::", ai_response)
    json_output = ai_response.choices[0].message.content

    return json_output
