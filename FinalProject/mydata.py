from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mydata.db'
db = SQLAlchemy(app)



# class Enrollment(db.Model):
#     __table__ = 'enrollment'
#     course_num = db.Column(db.Integer, db.ForeignKey('course.course_num'))
#     student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))


post_com = db.Table('post_com',
    db.Column('com_id ',db.Integer, db.ForeignKey('comment.com_id')),
    db.Column('post_id',db.Integer, db.ForeignKey('post.post_id')),
    #db.Column('name_id',db.Integer, db.ForeignKey('user.name_id'))
    
)
class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    post_des = db.Column(db.Text)
    posts = db .relationship('Comment',backref='post',lazy='dynamic')
    # def __repr__(self):
    #     return '<Post %r>' % self.post_des

class Comment(db.Model):
    __tablename__ = 'comment'
    com_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    com_des = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    #posts = db .relationship('Post', secondary=post_com,backref=db.backref('comments',lazy='dynamic'))

class Users(db.Model):
    __tablename__ = 'user'
    name_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nick_name = db.Column(db.Text)
    users = db .relationship('Comment',backref='user',lazy='dynamic')

    # def __repr__(self):
    #     return '<User %r>' % self.nick_name
    

   

#datetime.datetime.now()
#db.DateTime
#@app.route('/initdb')
#def fun():
db.drop_all()
db.create_all()

c1 = Comment(com_des='Brad')
c2 = Comment(com_des='Jane')
c3 = Comment(com_des='Josh')
db.session.add_all([c1,c2,c3])

x = "mary"
p1 = Post(post_des ='John')
p2 = Post(post_des ='John')
p3 = Post(post_des = x)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

#u1= User()


db.session.commit()

res = db.engine.execute('select * from post_com')
for row in res:
    print(row)
