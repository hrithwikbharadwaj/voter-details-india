from flask import Flask, request, jsonify
from extractFamilyDetails import start
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def helloWorld():
    return 'hello world', 200


@app.route('/', methods=['POST'])
def getFamilyDetails():
    data = request.json
    name = data["name"]
    dob = data['dob']
    state = data['state']
    gender = data['gender']
    relationName = data['relationName']
    if(state != "KA"):
        return "State Not Supported", 400
    res = start(name, dob, gender, relationName)
    return jsonify({"data": res})


if __name__ == '__main__':
    app.run()
