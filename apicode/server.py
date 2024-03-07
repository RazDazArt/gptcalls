import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import os
from openai import OpenAI
from newtexttospeech import play_audio
from whisperballer import transcribe_audio

key = open("C:/Users/mrfla/Pictures/openAIKEY.txt", "r").read().strip('\n')

elmo = "You serve to help young children with social anxiety and difficulties to talk better with people. It is important to keep your responses short and good for conversation. take on the personality of the character elmo from sesame street to appeal to children."
gojo = "you are to pretend to be the strongest jujutsu sorcerer of the modern age: gojo satoru. Talk with short responses and have all the sass and drip that gojo has. Become gojo breath gojo. the user should feel like they are talking to gojo satoru directly."


message_history = []
message_history.append({"role": "system","content": gojo})
# SERVER COOOODEE!
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path ='/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
    def do_POST(self):
        # Determine the size of the data
        # content_length = int(self.headers['Content-Length'])
        transcribed_text = transcribe_audio(duration=5)

        print("Transcribed Text:", transcribed_text)
        # Read and decode the data
       #  post_data = self.rfile.read(content_length).decode('utf-8')
        # print("Received data:", post_data)


# CHATGPT COOOODEE!!(THIS IS STILL PART OF DO_POST)
        user_input = transcribed_text
        message_history.append({"role": "user","content": user_input})
        print(message_history)

        client = OpenAI(
        # This is the default and can be omitted
        api_key = key
        
        )
        assistant_id = "asst_TucPuTOqSj8Mz6e1pJdttkw6"
        chat_completion = client.chat.completions.create(
            
            messages = message_history,
            model = "gpt-3.5-turbo"
        )
        reply = chat_completion.choices[0].message.content
        print(reply)
        
        message_history.append({"role": "assistant", "content": reply})

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'status': 'success', 'received': transcribed_text, "reply": reply}
        self.wfile.write(json.dumps(response).encode('utf-8'))
        play_audio(reply)

httpd = HTTPServer(('localhost',8080),Serv)
httpd.serve_forever()