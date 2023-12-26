import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import os
from openai import OpenAI
key = open("C:/Users/mrfla/Pictures/openAIKEY.txt", "r").read().strip('\n')

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
        content_length = int(self.headers['Content-Length'])

        # Read and decode the data
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("Received data:", post_data)



        client = OpenAI(
        # This is the default and can be omitted
        api_key = key
        )

        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": post_data,
            }
        ],
        model="gpt-3.5-turbo",
        )
        reply = chat_completion.choices[0].message.content
        print(reply)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'status': 'success', 'received': post_data, "reply": reply}
        self.wfile.write(json.dumps(response).encode('utf-8'))


httpd = HTTPServer(('localhost',8080),Serv)
httpd.serve_forever()