from flask import Flask, render_template, request, session,redirect, make_response,flash,jsonify
from flask_bootstrap import Bootstrap
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
import sqlite3
import psycopg2
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError
from jinja2.ext import do
from flask.ext.mail import Message, Mail
from datetime import datetime
import os

mail = Mail()
app = Flask(__name__)
Bootstrap(app)
app.jinja_env.add_extension('jinja2.ext.do')
app.debug = True   # need this for autoreload as well as stack trace
app.secret_key = 'luthercollege'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'norseconfessions@gmail.com'
app.config["MAIL_PASSWORD"] = 'n0rs3c0nf3ssi0ns'
mail.init_app(app)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mydata.db'
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI ='postgres://lyuutoxmemiolf:B9vTpATk6DfDJAmocb_iZWuHZp@ec2-54-225-101-119.compute-1.amazonaws.com:5432/d5jrjkt5lrtb1s'

db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    post_des = db.Column(db.Text)
    posts = db .relationship('Comment',backref='post',lazy='dynamic')

class Comment(db.Model):
    __tablename__ = 'comment'
    com_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    com_des = db.Column(db.Text)
    com_nickname = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.name_id'))

    #posts = db .relationship('Post', secondary=post_com,backref=db.backref('comments',lazy='dynamic'))

class User(db.Model):
    __tablename__ = 'user'
    name_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nick_name = db.Column(db.Text)
    users = db .relationship('Comment',backref='user',lazy='dynamic')


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    likenum = db.Column(db.Integer,default=0)
    dislikenum = db.Column(db.Integer,default=0)
    post_id = db.Column(db.Integer, default=0)

class ContactForm(Form):
  name = TextField("Name", [validators.Required("Please enter your name.")])
  email = TextField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your E-mail.")])
  subject = TextField("Subject", [validators.Required("Please enter a Subject.")])
  message = TextAreaField("Message", [validators.Required("Please enter a Message.")])
  submit = SubmitField("Send")

#db.drop_all()
#db.create_all()

@app.route('/')
def home():
  db.create_all()
  name = db.engine.execute('''select * from user''')
  nickname=[]
  for row in name:
    nickname.insert(0,row.nick_name)
  post = db.engine.execute('''select * from post''')
  posts =[]
  idlst =[]
  for row in post:
    posts.insert(0,row.post_des)
    idlst.insert(0,row.post_id)
  mydict1={}
  mydict2={}
  mydict3={}
  mydict4={}
  
  for i in idlst:
    res = db.engine.execute("select * from comment where post_id ="+str(i))
    #like = db.engine.execute("select * from like where post_id ="+str(i))
    l0 = Like(likenum = 0,dislikenum =0,post_id=i)
    db.session.add(l0)
    
   
    
    lst1=[]
    lst2=[]
    like = db.engine.execute("select * from like where post_id ="+str(i))
    likelst=[]
    dislikelst=[]
    for j in like:
      likelst.append(j.likenum)
      dislikelst.append(j.dislikenum)
    for row in res:
      lst1.append(row.com_nickname)
      lst2.append(row.com_des)
    mydict1[i] = lst1
    mydict2[i] = lst2
    mydict3[i]=likelst
    mydict4[i]=dislikelst


  like = db.engine.execute("select * from like ")
  likelst=[]
  for row in like:
    likelst.append(row)
  db.session.commit()

  return render_template('norse.html',nick_name=nickname,post=posts,mydict1=mydict1,mydict2=mydict2,likelst=likelst,mydict3=mydict3,mydict4=mydict4)



@app.route('/norseconfessions',methods=('GET', 'POST'))
def norse (name = None):
  nickName = request.form['nickname']
  desc = request.form['description']
  u1 = User(nick_name= nickName )
  p1 = Post(post_des = desc)
  db.session.add(u1)
  db.session.add(p1)
  db.session.commit()
  if 'babacookie' in request.cookies:
    return redirect('/')
  else:
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index )  
    response.set_cookie('babacookie',value=nickName)
    return response
    return redirect('/')
  #return render_template('norse.html',nick_name=nickName,post=desc)


@app.route('/comment',methods=('GET', 'POST'))
def comment(name = None):
  post = db.engine.execute('''select * from post''')
  posts =[]
  for row in post:
    posts.insert(0,row.post_des)
  nickName=""
  comm=""
  p = 0
  postId=0
  for i in range(len(posts)):
    while len(posts) >= p:
      try:
        nickName = request.form['commName'+str(i)]
        comm = request.form['userComment'+str(i)]
        postId=len(posts)-i
      except KeyError:
        pass
      p +=1
      i +=1
  c1 = Comment(com_des= comm,com_nickname=nickName,post_id=postId)
  db.session.add(c1)
  db.session.commit()
  #comments = db.engine.execute('''select * from comment''')
  #commlst =[]
  #for row in comments:
   # commlst.insert(0,row)
  #return render_template('norse.html',comments=commlst)
  return redirect('/')



@app.route('/like', methods=('GET', 'POST'))
def like(name = None):
  post = db.engine.execute('''select * from post''')
  posts =[]
  for row in post:
    posts.insert(0,row.post_des)
  p = 0
  for i in range(len(posts)):
    
  
    while len(posts) >= p:
      try:
        if request.form['like'+str(i)] == 'like':

          l1 = db.engine.execute("update like set likenum = likenum + 1 where post_id ="+str(len(posts)-i))
          #db.session.add(l1)
          db.session.commit()
          #db.close()
        elif request.form['like'+str(i)] == 'dislike':
          l2 =db.engine.execute("update like set dislikenum = dislikenum +1 where  post_id ="+str(len(posts)-i))
          #db.session.add(l2)
          db.session.commit()
      except KeyError:
        pass
      p+=1
      i+=1
      #db.close()
  return redirect('/')


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='norseconfessions@gmail.com', recipients=['patlra01@luther.edu','alcial01@luther.edu'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
  