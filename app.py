from flask import Flask, render_template, jsonify, redirect, request
import json
import random
import glob
import random
from chat import ChatGPTClone
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app = Flask(__name__, static_url_path='/static/')

# LECTURE_ID = "Random ID assigned to a lecture" this is generated from a file name?
# and probably a transcript txt file name too
# Conversation_ID = "ID associated with this conversation"

# Lecture info is stored in "lectures"
# Example lecture ID is "temp"

ACTIVE_CONVERSATION = {
    
}


@app.route('/newConversation', methods=['GET'])
@cross_origin()
def new_conversation():
    return {"message": "this is the start of the conversation"}

@app.route('/getListOfLectures', methods=['GET'])
@cross_origin()
def get_list_of_lectures():
    rr = list(set([x.split("/")[-1].partition(".")[0] for x in glob.glob("lectures/*")]))
    print(rr)
    return jsonify(
        {
            'data': rr
        })

@app.route('/getTranscript/<lecture_id>')
@cross_origin()
def get_transcript(lecture_id):
    return jsonify({
        'message': open('lectures/{}.txt'.format(lecture_id)).read()
    })

def gen_conversation_id(lecture_id):
    idVal = lecture_id + "_" + ''.join([str(random.randint(1,9)) for i in range(10)])
    ACTIVE_CONVERSATION[idVal] = ChatGPTClone(open('lectures/{}.txt'.format(lecture_id)).read())
    return idVal

@app.route('/generateConversationId/<lecture_id>', methods=['GET'])
@cross_origin()
def get_conversation_id(lecture_id):
    return jsonify({
        'message': gen_conversation_id(lecture_id)
    })

@app.route('/newConversation', methods=['GET'])
@cross_origin()
def create_new_conversation():
    return

import re

def extract_percentage(string):
    try:
        x = re.findall("(\d+)%", string)
        x = int(x)
    except:
        x = random.randint(1, 100)
    return int(x)


@app.route("/extractRecentPercentage/<conversation_id>", methods=['POST'])
def extract_from_percent(conversation_id):
    prompt = "Where in the lecture was this found? Give me your respose to this question as a percentage of how far into the text this location is."
    response = ACTIVE_CONVERSATION[conversation_id].add_and_submit(prompt)
    return jsonify({
        'percent': extract_percentage(response)
    })

@app.route('/askQuestion/<conversation_id>', methods=['POST'])
@cross_origin()
def ask_question(conversation_id):
    question = request.get_json().get("question")
    if conversation_id not in ACTIVE_CONVERSATION:
        return jsonify({"message": "conversation does not exist..."})
    
    return jsonify({"message": ACTIVE_CONVERSATION[conversation_id].add_and_submit(question)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)