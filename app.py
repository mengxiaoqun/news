#!/usr/bin/env python3

from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/news'

db = SQLAlchemy(app)
client = MongoClient('127.0.0.1',27017)
mongo = client.news


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

    
    def add_tag(self,tag_name):
        result = mongo.files.find_one({'id':self.id})
        if result:
            tags = result['tags']
            if tag_name not in tags:
                tags.append(tag_name)
                mongo.files.update_one({'id':self.id},{'$set':{'tags':tags}})
            return tags
        else:
            mongo.files.insert_one({'id':self.id,'tags':[tag_name]})
            return [tag_name]
    
    def remove_tag(self,tag_name):
        result = mongo.files.find_one({'id':self.id})
        if result:
            tags = result['tags']
            if tag_name in tags:
                tags.remove(tag_name)
                mongo.files.update_one({'id':self.id},{'$set':{'tags':tags}})
                return tags
        else:
            return []

    @property
    def tags(self):
        result = mongo.files.find_one({'id':self.id})
        if result:
            return result['tags']
        else:
            return []



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
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


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
