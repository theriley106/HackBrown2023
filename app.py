from flask import Flask, render_template, jsonify, redirect
import json
import random


app = Flask(__name__, static_url_path='/static/')

# LECTURE_ID = "Random ID assigned to a lecture" this is generated from a file name?
# and probably a transcript txt file name too
# Conversation_ID = "ID associated with this conversation"

# Lecture info is stored in "lectures"
# Example lecture ID is "temp"

@app.route('/newConversation', methods=['GET'])
def new_conversation():
    return {"message": "this is the start of the conversation"}

@app.route('/getListOfLectures', methods=['GET'])
def get_list_of_lectures():
    return list(set([x.split("/")[-1].partition(".")[0] for x in glob.glob("lectures/*")]))


@app.route('/newConversation', methods=['GET'])
def create_new_conversation():
    return

@app.route('/askQuestion/<conversation_id>', methods=['POST'])
def ask_question():
    return {"message": "this is the start of the conversation"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)