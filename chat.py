import os
import openai
try:
    from keys import *
except:
    API_KEY = input("OpenAI Key: ")

openai.api_key = API_KEY

TRANSCRIPT = open("transcript.txt").read()

# Pass in a "Modified" prompt (with the chat history from before)
def fetch_openai_response(prompt):
    start_sequence = "\nAI:"
    restart_sequence = "\nStudent: "
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Student:", " AI:"]
    )
    
    return response['choices'][0]['text'].strip()

START_PROMPT = """
You are an AI model that is trained on a classroom lecture in a university setting. I will feed you the
transcript of your lecture today.

At periods of time, I will feed you questions from students in the lecture. These questions will begin
with "Student: ". You will response concisely from the perspective of the professor teaching the course. 
The lecture is as followed:
""".replace("\n", " ")

class ChatGPTClone():
    def __init__(self, lecture):
        # You probably don't need to feed it any lecture to begin
        self.prompt = START_PROMPT + "\n" + lecture 
        self.prompt = " ".join(self.prompt.split(" ")[:4000])
        
        self.prompt += "\n"

        self.last = []

    def add_to_prompt(self, text):
        xr = "Student: " + text + "\nAI: "
        self.last.append(xr)
        self.prompt += xr



    def submit(self, ai_part=True):
        # print(self.last[-1], end=" ")
        rr = fetch_openai_response(self.prompt)
        if ai_part:
            return "AI: " + rr
        return rr
        

    def add_and_submit(self, text):
        self.add_to_prompt(text)
        temp = self.prompt.split(" ")

        xre = self.prompt.index("followed:")
        while len(temp) > 3000:
            try:
                temp.pop(xre + 1)
            except:
                temp.pop(-1)
        self.prompt = " ".join(temp)

        x = self.submit(False)
        while len(x) == 0:
            print("REPEATING FOR SOME REASON??")
            x = self.submit(False)
        self.prompt += x + "\nStudent: "
        return x

    

if __name__ == "__main__":
    A = ChatGPTClone(TRANSCRIPT)

    newPrompt = "test"

    while len(newPrompt) > 0:
        newPrompt = input("Client: ")
        A.add_to_prompt(newPrompt)
        print(A.submit())