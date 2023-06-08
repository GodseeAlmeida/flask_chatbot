from flask import Flask, render_template, request, copy_current_request_context
import openai
import pyttsx3
import time
import threading


app = Flask(__name__)

# Set up your OpenAI API credentials
openai.api_key = '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'

def send_message(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    reply = response.choices[0].text.strip()
    return reply

def text_to_speech(reply):
    # Initialize the speech synthesis engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust the speech rate if needed

    # Convert the reply to speech
    engine.say(reply)
    engine.runAndWait()

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        condition = request.form['condition']
        severity = request.form['severity']
        message = f"Health condition: {condition}\nSeverity: {severity}"
        reply = send_message(message)

        # Render the template with the initial response
        rendered_template = render_template('index.html', reply=reply)
        
        @copy_current_request_context
        def delayed_speech_synthesis():
            # Delay the speech synthesis to allow the response to be displayed in the browser
            time.sleep(10)

            # Convert the reply to speech
            text_to_speech(reply)

        # Start a separate thread to perform the delayed speech synthesis
        threading.Thread(target=delayed_speech_synthesis).start()

        # Return the rendered template
        return rendered_template

    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
