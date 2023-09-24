import json
from flask import Flask, request, jsonify, Response
from unstructured_model import get_question_score, gpt_res
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
CORS(app, origins="*")

fileContent = []

@app.route('/api/file', methods=['POST'])
def file():
    def extract_file_content(file_contents) :
        global fileContent
        try:
            response_json = gpt_res(file_contents)
            fileContent = json.loads(response_json)
            print("data extracted::::::::::::::::")
            return "data extracted"

        except Exception as e:
            print("An error occurred:", str(e))

    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    print("file received::::::::::::::::")

    file_contents =file.read().decode("utf-8")
    if(extract_file_content(file_contents) == "data extracted"):
        return jsonify({"message" : "data extracted"}), 200
    
    return jsonify({"message" : "error while extracting data"}), 400


@app.route('/api/score')
def score():
    global fileContent
    def generate_stream():
        if(len(fileContent) > 0) :
            for content in fileContent :
                question = content.get("question", "")
                answer = content.get("answer", "")
                new_score = get_question_score(question, answer)
                valid_json_string = new_score.replace("'", "\"")
                valid_json = json.loads(valid_json_string)
                # jsonScore = json.dumps(new_score)
                data = {"question" : question, "answer" : answer, "score" : valid_json.get("score"), "reason" : valid_json.get("reason")}
                jsonData = json.dumps(data)
                print("jsonData:::::::::",jsonData)
                yield f"data: {jsonData}\n\n"

    return Response(generate_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)
