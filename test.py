import requests

headers = {
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
}



def get_list_of_lectures():
    return requests.get('http://hackbrown.ngrok.io/getListOfLectures').json()


def get_new_conversation_id(lecture):
    return requests.get('http://hackbrown.ngrok.io/generateConversationId/{}'.format(lecture)).json()


def ask_question(idVal, question):
    json_data = {
        'question': question,
    }

    return requests.post('http://hackbrown.ngrok.io/askQuestion/{}'.format(idVal), headers=headers, json=json_data).json()

if __name__ == "__main__":
    lecture_id = get_list_of_lectures()['data'][1]
    conversation_id = get_new_conversation_id(lecture_id)['message']
    print(conversation_id)
    input("AYY")
    while True:
        question = input("Question: ")
        print(ask_question(conversation_id, question))