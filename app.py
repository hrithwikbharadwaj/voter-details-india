from flask import Flask, request, jsonify
from extractFamilyDetails import start
from flask_cors import CORS
from dotenv import load_dotenv
from treebuilder import getSampleData, getFamilyTree
from utils import validateStringNotEmpty

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def helloWorld():
    return 'hello world', 200


@app.route('/', methods=['POST'])
def getFamilyDetails():
    data = request.json

    nameValidation = validateStringNotEmpty("name", data)
    if nameValidation:
        return nameValidation
    dobValidation = validateStringNotEmpty("dob", data)
    if dobValidation:
        return dobValidation
    stateValidation = validateStringNotEmpty("state", data)
    if stateValidation:
        return stateValidation
    genderValidation = validateStringNotEmpty("gender", data)
    if genderValidation:
        return genderValidation
    relationValidation = validateStringNotEmpty("relationName", data)
    if relationValidation:
        return relationValidation

    name = data["name"]
    dob = data['dob']
    state = data['state']
    gender = data['gender']
    relationName = data['relationName']
    if(state != "KA"):
        return "State Not Supported", 400
    res = start(name, dob, gender, relationName)
    return jsonify({"data": res})


@app.route('/sample', methods=['GET'])
def getSampleFamilyTree():
    sampleInput = getSampleData()
    familyTree = getFamilyTree(getSampleData())
    return jsonify({"sampleInput": sampleInput, "familyTree": familyTree})


if __name__ == '__main__':
    app.run()
