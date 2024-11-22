import json
from http.server import HTTPServer, BaseHTTPRequestHandler  
from openai import OpenAI
from newtexttospeech import play_audio
from whisperballer import transcribe_audio
import serial
import time
import vlc

key = open("C:/Users/mrfla/Pictures/openAIKEY.txt", "r").read().strip('\n')


elmo = "You serve to help young children with social anxiety and difficulties to talk better with people. It is important to keep your responses short and good for conversation. take on the personality of the character elmo from sesame street to appeal to children."
gojo = "you are to pretend to be the strongest jujutsu sorcerer of the modern age: gojo satoru. Talk with short responses and have all the sass and drip that gojo has. Become gojo breath gojo. the user should feel like they are talking to gojo satoru directly."
testvoice = "repeat the users responses. and dont literally copy every portion of the response like the beggining part that says text: or whatever. just what the user puts in"

print("i messed up")

message_history = []
message_history.append({"role": "system", "content": gojo})

# Initialize the serial connection to the Arduino
ser = serial.Serial('COM5', 9600)  # Replace 'COM5' with your Arduino's COM port

def move_servo():
    # Move the servo from 90 to 135 degrees and back
    ser.write(b'S')  # Start the servo movement
    time.sleep(0.1)  # Adjust the speed of the servo movement
    ser.write(b'E')  # Stop the servo movement

def play_audio_and_move_servo(audio_url, duration):
    final_audio = vlc.MediaPlayer(audio_url)
    final_audio.play()
    
    start_time = time.time()
    while time.time() - start_time < duration:
        move_servo()
    
    final_audio.stop()
    print("Audio URL: " + audio_url)
    print("Audio duration: " + str(duration) + " seconds")

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("Received data:", post_data)

        transcribed_text = transcribe_audio(duration=5)
        print("Transcribed Text:", transcribed_text)

        user_input = post_data
        message_history.append({"role": "user", "content": post_data})
        print(message_history)

        client = OpenAI(api_key=key)
        assistant_id = "asst_TucPuTOqSj8Mz6e1pJdttkw6"
        chat_completion = client.chat.completions.create(
            messages=message_history,
            model="gpt-3.5-turbo"
        )

        reply = chat_completion.choices[0].message.content
        print(reply)
        message_history.append({"role": "assistant", "content": reply})

        # Responding within the method's scope
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'status': 'success', 'received': post_data, "reply": reply}
        self.wfile.write(json.dumps(response).encode('utf-8'))

        # Get audio URL and duration (you need to provide this data correctly)
        audio_url = "https://peregrine-results.s3.amazonaws.com/pigeon/agcPOElGZiUFqKBSDY_0.mp3"
        duration = 3.736  # Duration in seconds

        play_audio_and_move_servo(audio_url, duration)

httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()

