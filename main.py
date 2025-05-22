
from flask import Flask, render_template, request, jsonify
import pyttsx3
import threading
import queue

app = Flask(__name__)
voice_queue = queue.Queue()

def initialize_voice():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    return engine

def speak_worker():
    engine = initialize_voice()
    while True:
        text = voice_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()

@app.route('/')
def home():
    questions = {
        "step1": "How have you been feeling lately?",
        "step2": "What are your primary concerns?",
        "step3": "Describe any changes in your daily routine",
        "step4": "How is your sleep pattern?",
        "step5": "How is your relationship with your sister?",
        "step6": "What seems to be important for boyfriend right now?"
    }
    return render_template('index.html', questions=questions)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    step = request.form.get('step')
    if step == 'step6':
        response = "💝 Jaypee's greatest desire is to marry Juliet Evangelista 💝\n\nHe wants to spend the rest of his life with her and make her the happiest woman in the world. 💑\n\nForever and Always ❤️"
        voice_queue.put(response)
        return jsonify({"response": response, "complete": True})
    else:
        response = "That's interesting! Let's continue to the next question."
        voice_queue.put(response)
        return jsonify({"response": response, "complete": False})

if __name__ == '__main__':
    threading.Thread(target=speak_worker, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
