from flask import render_template

from portra.app import app

@app.route('/', methods={'GET', 'POST'})
def home():
    return 'test'
