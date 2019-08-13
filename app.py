#!/usr/bin/env python3

from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/news'

db = SQLAlchemy(app)


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    category = db.relationship('Category',uselist=False)
    content = db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title = title
        if created_time is None:
            self.created_time = created_time
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File %r>' % self.title


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    files = db.relationship('File')

    def __repr__(self):
        return '<Category %r>' % self.name

def create_data():
    java = Category(name='Java')
    python = Category(name='Python')
    file1 = File('Hello Java', datetime.utcnow(), java,'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python,'File Content - Python is cool!')
    db.session.add(java)

    db.session.add(file2)
    db.session.commit()


@app.route('/')
def index():
    data = File.query.all()
    return render_template('index.html',data=data)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

@app.route('/files/<file_id>')
def file(file_id):
    data = File.query.get_or_404(file_id)
    return render_template('file.html',data=data)


if __name__ == '__main__':
    app.run()
