from flask import Flask
from .finderphrases import FinderPhrases
from flask import request
from flask import render_template, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'st02300dfdsfdsfdsfeadasdeadafdasfesdfeadas'



@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        links_and_contents = FinderPhrases().get_phrases(content, 5)
        if not content:
            flash('Title is required!')
        return render_template('movies.html', context=links_and_contents)

    return render_template('home.html')





