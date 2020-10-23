from flask import Flask, render_template, jsonify, make_response, g, request
import psycopg2 # driver for postgresql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


POSTGRES_USER="tabs"
POSTGRES_PW="tabs"
POSTGRES_URL="db3"
POSTGRES_PORT="3406"
POSTGRES_DB="tabsdb"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}'.format(user=POSTGRES_USER,
                                                                                                    url=POSTGRES_URL,    
                                                                                                    pw = POSTGRES_PW,                                                                                           
                                                                                                    port=POSTGRES_PORT,
                                                                                                    db=POSTGRES_DB)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # adds significant overhead

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# engine = create_engine("postgresql://tabs:pwd@localhost:5432/sammy", echo=True)

#class that creates a db
class Post(db.Model):
    __tablename__ = 'post'
    title = db.Column(db.String(200))
    content_post = db.Column(db.String(2000))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, title, content_post):
        self.title = title
        self.content_post = content_post

def database_initialization_sequence():
    Base = declarative_base()
    Base.metadata.create_all(engine)
    test_rec = Post('DemoPost',
            'Demo post is working fine')

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


#REST API
#Get record
@app.route("/id/<int:id>", methods= ["GET"])
def getData(id = None):
    try:
        toget = Post.query.get(id)
        return jsonify({'id':toget.id,
                        'title':toget.title,
                        'content_post':toget.content_post})

        # return jsonify(toget)
    except:
        return 'No record exists in the db matching the id'

#updated content_post is added in the body of the PUT request
@app.route("/update/<int:id>", methods= ["POST"])
def putData(id = None):
    #check if the title exists in the Db
    toupdate = Post.query.get_or_404(id)
    if toupdate:
        toupdate.content_post = request.json['content_post']
        db.session.commit()
        return "Sucessfully updated the record"

#Add new records
@app.route("/add", methods= ["POST"])
def postData(title = None, content_post = None):
    p1 = Post(title=request.json['title'],content_post=request.json['content_post'])
    db.session.add(p1)
    db.session.commit()
    return "Succesfully sent to the DB"

#Delete record
@app.route("/delete/<int:id>", methods= ["DELETE"])
def deleteData(id = None):
    todelete = Post.query.get_or_404(id)
    db.session.delete(todelete)
    db.session.commit()
    return "Succesfully deleted from the DB"
    

if __name__ == '__main__':
    # database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
