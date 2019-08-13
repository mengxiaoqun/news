#!/usr/bin/env python3
from flask import Flask,render_template,abort,json
import os

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files/<filename>')
def files(filename):
    return render_template('file.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
