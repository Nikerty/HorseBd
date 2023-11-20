from flask import Flask, request, jsonify, json
from .main import assistant
from answer_creating import assistant

app = Flask(__name__)


@app.route("/", methods=['POST'])
def assistant_route():
    rq = json.loads(request.get_data(as_text=True))['question']
    rs = assistant(rq)
    return jsonify(response=rs)

@app.route("/answer", methods=['GET'])
def main_route():
    rq = json.loads(request.get_data(as_text=True))['question']
    rs = assistant(rq)
    return jsonify(response=rs)
