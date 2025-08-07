from flask import Flask, render_template, request, session
import cohere
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for session to work

co = cohere.Client("Ft7jtn36aHpXEF2e7E1dyomcwRT5GXDWO0SRwYRV")  # Replace with your actual API key

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        question = request.form['question']
        response = co.generate(
            model='command-light',
            prompt=question,
            max_tokens=100
        )
        answer = response.generations[0].text.strip()

        # Add to history
        session['history'].append({'question': question, 'answer': answer})
        session.modified = True  # Important to save session changes

    return render_template('index.html', history=session['history'])

if __name__ == '__main__':
    app.run(debug=True)
