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

import urllib.parse
app = Flask(__name__, static_folder='lectures')

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
import random

def extract_percentage(string):
    try:
        x = re.findall("(\d+)%", string)[0]
        x = int(x)
    except Exception as exp:
        print(exp)
        x = random.randint(1, 100)
    return int(x)


from moviepy.editor import VideoFileClip

def with_moviepy(filename):
    clip = VideoFileClip(filename)
    duration       = clip.duration
    fps            = clip.fps
    width, height  = clip.size
    return duration, fps, (width, height)

import time
@app.route("/extractRecentPercentage/<conversation_id>", methods=['POST', "GET"])
@cross_origin()
def extract_from_percent(conversation_id):
    filename = "lectures/" + conversation_id.partition("_")[0] + ".mp4"
    
    prompt = "Where in the lecture was this found? Give me your respose to this question as a percentage of how far into the lecture this location is."
    response = ACTIVE_CONVERSATION[conversation_id].add_and_submit(prompt)
    print(response)
    xr = int(with_moviepy(filename)[0] * (extract_percentage(response) / 100))
    print(xr)
    time.sleep(1)
    return jsonify({
        'percent': xr
    })

@app.route('/askQuestion/<conversation_id>', methods=['POST'])
@cross_origin()
def ask_question(conversation_id):
    question = request.get_json().get("question")
    if conversation_id not in ACTIVE_CONVERSATION:
        return jsonify({"message": "conversation does not exist..."})
    
    return jsonify({"message": ACTIVE_CONVERSATION[conversation_id].add_and_submit(question)})

@app.route('/', methods=['GET'])
def index():
    rr = list(set([x.split("/")[-1].partition(".")[0] for x in glob.glob("lectures/*.mp4") if 'temp' not in x]))
    return render_template("index.html", values=rr)
    return jsonify({"message": ACTIVE_CONVERSATION[conversation_id].add_and_submit(question)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)