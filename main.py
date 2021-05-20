from random import randint, choice, shuffle, sample
from flask import Flask, render_template, request, session
from tasks import *


def start():
    session.clear()
    session['points'] = 0
    session['answered'] = []
    session['options'] = []
    # print(session)

def get_topic_tasks(topic):
    topic_tasks = tasks[topic].copy()
    shuffle(topic_tasks)
    session['tasks'] = topic_tasks


def get_current_task():
    while True:
        task = choice(session['tasks'])
        if task not in session['answered']:
            break
    
    session['current_task'] = task
    session['right'], session['question'] = task

   
def form_options():
    session['options'].clear()
    task = session['current_task']
    variants = session['tasks'].copy()
    variants.remove(task)
    session['options'].append(task)
    session['options'].extend(sample(variants, 3))
    shuffle(session['options'])


app = Flask(__name__)
app.secret_key = 'top_secret'


@app.route('/')
def index():
    start()
    return render_template('index.html')

@app.route('/task')
def task():
    if 'topic' in request.args:
        session['topic'] = request.args.get('topic')
    if 'tasks' not in session:
        get_topic_tasks(session['topic'])
    
    if len(session['tasks']) > len(session['answered']):
        get_current_task()
        form_options()
        print(session)
        return render_template('task.html', topic=session['topic'], items=session['options'], question=session['right'], filename=session['right'])
    else:
        return render_template("finished.html")


@app.route('/result')
def result():
    right_phrases = (
        "Great!", "Right!", "Yes!",
        "Excellent!", "You are right!"
        )

    wrong_phrases = (
        "No!", "It's wrong!", "Mistake!",
        "You are wrong!", "It's not right!"
        )

    answer = request.args.get('answer')
    if answer == session['right']:
        session['points'] += 1
        session['answered'].append(session['current_task'])
        session['current_task'] = None
        return render_template("right.html",points=session['points'], right=choice(right_phrases))
    else:
        session['answered'].append(session['current_task'])
        session['current_task'] = None
        return render_template("wrong.html", wrong=choice(wrong_phrases))

app.run(host="0.0.0.0")