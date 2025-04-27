from flask import Flask, render_template, request, session, redirect, url_for
from openai import OpenAI
import json
app = Flask(__name__)

app.secret_key = 'abcdef'

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/quiz', methods = ["GET", "POST"])
def quiz(): # session = {} --> session = {'quiz': ["quiz1","quiz2,]..}
    quiz_data = session.get("quiz", [])
    if quiz_data == []:
        sample = "The first little pig was very lazy. He didn't want to work at all and he built his house out of straw. The second little pig worked a little bit harder but he was somewhat lazy too and he built his house out of sticks. Then, they sang and danced and played together the rest of the day."
        quiz = generate_quiz(sample)
        session["quiz"] = quiz # session = {'quiz': 5 questions}
        session["current_question"] = 0 # session = {'quiz': 5 questions, 'current_question':0}
        quiz_data = quiz
    index = session.get("current_question", 0)
    if request.method == "POST": # when user submit the answer
        selected = request.form.get("answer")
        index += 1 # increase index by 1
        session["current_question"] = index
        if index >= len(quiz_data):
            return render_template('complete.html')
        return redirect(url_for("quiz"))
    if index < len(quiz_data):
        question = quiz_data[index]
        return render_template('quiz.html',question=question, index=index )
    return render_template('quiz.html')

def generate_quiz(story_text):
    prompt = f"""
        Generate 5 multiple choice quiz questions based on the following story.
        {story_text}
        Format:
        [
            {{
                "question": "What is the capital of South Korea?",
                "options:" ["London","Paris", "Seoul", "Tokyo"],
                "answer": "Seoul"
            }}   
        ]
    """
    response = client.chat.completions.create(
        model = "gpt-4",
        messages = [
            {'role':'system', 'content': 'You are a elementary school instructor. Please use easy vocabulary to generate quiz questions'},
            {'role':'user', 'content': prompt}
        ],
        temperature = 0.7
    )
    content = response.choices[0].message.content.strip()
    return json.loads(content)

if __name__ == "__main__":
    # story = "The first little pig was very lazy. He didn't want to work at all and he built his house out of straw. The second little pig worked a little bit harder but he was somewhat lazy too and he built his house out of sticks. Then, they sang and danced and played together the rest of the day."
    # print(generate_quiz(story))
    app.run(debug=True)

