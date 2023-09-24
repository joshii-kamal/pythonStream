from flask import Flask, request, Response
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with supports_credentials=True for cookie-based authentication if needed


# datas = [
#             {
#                 "question" : "hey what is you name?",
#                 "answer" : "my name is kamal chandra joshi",
#                 "score" : "9/10",
#                 "reason" : "noice name"
#             },
#             {
#                 "question" : "hey what is you age?",
#                 "answer" : "my age is 30",
#                 "score" : "9/10",
#                 "reason" : "old enough"
#             },
#             {
#                 "question" : "hey what do you do?",
#                 "answer" : "i code",
#                 "score" : "9/10",
#                 "reason" : "noice job"
#             },
#         ]

data = [
    1,2,3,4,5,6,7,8,9,0
]

@app.route('/api/file', methods=['POST'])
def file():
    # here we have use the gpt code to extrace the question and answer
    global data
    file = request.files['file']
    
    file_content = file.read().decode('utf-8').splitlines()
    print("file content:::::", file_content)
    data = file_content
    return "UPLOADED SUCESSFULLY"

@app.route('/api/stream')
def stream():
    # this will be used for continous streaming
    global data

    print("Data::::::::::",data)
    for i in range(1,3):
        print("i::::::",i)
        time.sleep(2)
    
    def generate_stream():
        i = 0
        if(len(data) > 0) :
            while i < 10 :
            # for line in data:
                time.sleep(2)
                # json_data = json.dumps(line)
                # result = gpt(question ,answer)
                print(i)
                i +=1
                yield f"data: {i}\n\n"
                  
    return Response(generate_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/api/upload/file', methods=['POST'])
# def check():
#     file = request.files['file']

#     def readFile(file):
#         try:
#             with file.stream as file_stream:
#                 for line in file_stream:
#                     yield f'data: {line.decode("utf-8").strip()}\n'
#                     time.sleep(2)  # Optional delay between sending lines
#         except Exception as e:
#             yield f'data: Error: {str(e)}\n'
#
    # return Response(readFile(file), mimetype='text/event-stream')