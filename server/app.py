#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

##instructions: when a user makes a get request, if this is the first request, 
#set session['page_views'] to an initial value of 0.
#for every request, increment session['page_views'] by 1
#If user has viewed 3 or less pages, render a JSON response with article data
#else send a message and status code 401
@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views') or 0
    session['page_views'] += 1

    if session['page_views'] <= 3:
        article = Article.query.filter_by(id=id).first()
        return make_response(article.to_dict(), 200)
    
    return {"message": "Maximum pageview limit reached"}, 401
        

    

if __name__ == '__main__':
    app.run(port=5555)
