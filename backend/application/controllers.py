# from flask import Flask, request, redirect, flash
# from flask import render_template
from flask import request
from flask import current_app as app
from flask import jsonify
from application.models import User, Card, List
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from application.database import db
from datetime import datetime, date
from application import tasks
# from flask.helpers import url_for
# from application.models import *
# from flask_login import login_user, login_required, logout_user, current_user
# from application.forms import RegistrationForm, LoginForm
# from main import bcrypt
# from application.database import db
# from main import login_manager
# import random
# from application.helperfunction import  utc_to_local
# from datetime import datetime, timedelta
# import pytz
# IST = pytz.timezone('Asia/Kolkata')


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))
@app.route('/test123',methods=['GET','POST'])
@jwt_required()
def index():
    current_user=get_jwt_identity()
    print(current_user)
    deadline=request.get_json()['deadline']
    print(deadline)
    year,month, day=map(int,deadline.split('-'))
    print(year,month,day)
    deadlinedate=date(year, month, day)
    print(deadlinedate,type(deadlinedate))
    time_now = date.today()
    print(time_now,type(time_now))
    days=(time_now-deadlinedate).days
    print(days,type(days))
    datestr=time_now.strftime('%Y-%m-%d')
    print(datestr)
    # user = User.query.filter_by(username=current_user).first()
    # if not user:
    #     return {"msg": "User not found"}
            
    # lists = List.query.filter_by(user_id=user.user_id).all()
    # if len(lists)==0:
    #     return {"msg": "No list created for the user"}
    # else:
        
    #     return {"lists":[{
    #         "id": list.id,
    #         "title": list.title,
    #         "user_id": list.user_id,
    #     } for list in lists]}
    return {'deadline':datestr}
@app.route('/api/card/complete/<int:card_id>',methods=['GET','POST'])
@jwt_required()
def cardComplete(card_id):
    card= Card.query.filter_by(id=card_id).first()
    if not card:
        return{'status':False,'error_message':'Card not found'},401
    if card.completed==0:
        card.completed=1
        card.completed_time=date.today()
    else:
        card.completed=0
        card.completed_time=None
    db.session.commit()
    return {'status':True},200

@app.route('/hello/<username>',methods=['GET','POST'])
def hello(username):
    job=tasks.just_say_hello.delay(username)
    return str(job),200   
# @app.route("/register", methods=["GET", "POST"])
# def register():
    
#     if current_user.is_authenticated:
#         return redirect("/")
#     form = RegistrationForm()
    
#     if form.validate_on_submit():
        
#         user = User(username=form.username.data)
#         user.password=bcrypt.generate_password_hash(form.password.data)

#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect("/login")
    
#     return render_template('register.html', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
    
#     if current_user.is_authenticated:
#         return redirect("/")
#     form = LoginForm()
    
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not bcrypt.check_password_hash(user.password,form.password.data):
#             flash('Invalid username or password')
#             return redirect("/login")
#         user.active=1
#         db.session.commit()
#         login_user(user, remember=form.remember_me.data)
        
#         return redirect("/")
#     return render_template('login.html', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#     u = User.query.get(current_user.id)
#     u.active=0
#     db.session.commit()
#     logout_user()
#     flash('You have been logged out')
#     return redirect(url_for('login')) 

# @app.route('/')
# @login_required
# def index():
    
#     u = User.query.get(current_user.id)
#     time_now = datetime.utcnow()
#     decks = Deck.query.filter_by(user_id=u.id).all()
#     cardnum=[]
#     scores=[]
#     reviews=[]
#     review_time_ist=[]
#     for deck in decks:
#         cards = Card.query.filter_by(deck_id=deck.id).all()
#         # print(timedelta(hours=1)+deck.review_time)
#         # print(time_now)
#         # print((timedelta(hours=1)+deck.review_time)<time_now)
#         if len(cards)==0:
#             score=0
#             reviews.append(False)

#         elif deck.review_time==None or (timedelta(hours=1)+deck.review_time<time_now) :
#             deck.deck_score=0
#             db.session.add(deck)
#             score=deck.deck_score
#             for card in cards:
#                 card.review=0
#             db.session.add(card)
#             reviews.append(True)
            
#         else:
#             score = int(round((deck.deck_score/len(cards))*100))
#             reviews.append(False)
#         if deck.review_time is None:
#             review_time_ist.append(None)
#         else:
#             review_time_ist.append(utc_to_local(deck.review_time))
#         scores.append(score)
#         cardnum.append(len(cards))
#     db.session.commit()
#     return render_template('index.html', decks=decks, cardnum=cardnum, scores=scores, reviews=reviews, review_time_ist=review_time_ist)

# @app.route('/deck/add', methods=['GET', 'POST'] )
# @login_required
# def deck():
#     u = User.query.get(current_user.id)
#     if request.method=='POST':
#         title = request.form['title']
#         deck =Deck.query.filter((Deck.title==title) & (Deck.user_id==u.id)).first()
#         if not deck:
#             deck = Deck(title=title, user_id=u.id)
#             db.session.add(deck)
#             db.session.commit()
#             return redirect('/')
        
            
#     return render_template('deckadding.html')

# @app.route('/deck/<int:deck_id>/delete')
# @login_required
# def deck_delete(deck_id):
#     deck = Deck.query.filter_by(id=deck_id).first()
    
#     if  deck:
#         cards = Card.query.filter_by(deck_id=deck.id).all()
#         if len(cards)>0:
#             for card in cards:
#                 db.session.delete(card)
#         db.session.delete(deck)
#         db.session.commit()
#         return redirect('/')
#     return redirect('/')


# @app.route('/deck/<int:deck_id>/card/add',methods=['GET','POST'])
# @login_required
# def card_add(deck_id):
#     deck = Deck.query.filter_by(id=deck_id).first()
#     if request.method =='POST':
#         front = request.form['front']
#         back = request.form['back']
#         if  deck:
#             card = Card(front=front, back=back, deck_id=deck_id)
#             card.review=0
#             db.session.add(card)
#             db.session.commit()
#             return redirect('/')
#     return render_template('addcard.html',deck_id=deck_id)


# @app.route('/deck/<int:deck_id>/test')
# @login_required
# def test(deck_id):
#     deck = Deck.query.filter_by(id=deck_id).first()
#     UTC_datetime = datetime.now()
#     # UTC_datetime_timestamp = float(UTC_datetime.strftime("%s"))
#     # local_datetime_converted = datetime.fromtimestamp(UTC_datetime_timestamp)
#     deck.review_time = datetime.utcnow()

#     db.session.add(deck)
#     db.session.commit()
#     cardlen = len(Card.query.filter_by(deck_id=deck.id).all())
#     score = int(round((deck.deck_score/cardlen)*100))
#     if deck:
#         cards =Card.query.filter_by(deck_id=deck.id, review=0).all()
#         cardnum = len(cards)
#         if cardnum == 0:
#             return render_template('test.html',deck=deck,cardnum=cardnum, cardlen=cardlen,score=score)
        
#         i=random.randrange(cardnum)
#         card=cards[i]
#         cardId= card.id
        
#         return render_template('test.html',deck=deck, cardnum=cardnum,card=card, cardlen=cardlen,score=score)


# @app.route('/deck/<int:deck_id>/learn/<int:cardId>/notknow')
# @login_required
# def notknow(deck_id, cardId):
#     card = Card.query.filter_by(id=cardId).first()
#     card.review = 1
#     deck = Deck.query.filter_by(id=deck_id).first()
#     db.session.add(card)
#     db.session.commit()
#     return redirect(url_for('.test', deck_id=deck_id))


# @app.route('/deck/<int:deck_id>/learn/<int:cardId>/know')
# @login_required
# def know(deck_id, cardId):
#     card = Card.query.filter_by(id=cardId).first()
    
#     card.review = 1
#     u = User.query.get(current_user.id)
#     deck = Deck.query.filter_by(id=deck_id).first()
#     cards = Card.query.filter_by(deck_id=deck.id).all()
#     cardnum = len(cards)
#     deck.deck_score+=1
#     db.session.add(deck)
#     db.session.add(card)
#     db.session.commit()
#     return redirect(url_for('.test', deck_id=deck_id))

# @app.route('/deck/<int:deck_id>/update')
# @login_required
# def deck_update(deck_id):
#     deck = Deck.query.filter_by(id=deck_id).first()
#     cards = Card.query.filter_by(deck_id=deck.id).all()
#     print(deck)
#     return render_template('showcard.html', deck=deck, cards=cards)


# @app.route('/deck/<int:deck_id>/edit', methods = ['GET','POST'])
# @login_required
# def deck_edit(deck_id):
#     deck = Deck.query.filter_by(id=deck_id).first()
#     cards = Card.query.filter_by(deck_id=deck.id).all()
#     if request.method =='POST':
#         title = request.form['title']
#         deck.title = title
#         db.session.add(deck)
#         db.session.commit()
#         return redirect(url_for('.deck_update', deck_id=deck_id))
#     return render_template('deckupdate.html', deck=deck)
#     # if  deck:
#     #     db.session.delete(deck)
#     #     db.session.commit()
#     #     return redirect('/')
#     # return redirect('/')
# @app.route('/card/<int:card_id>/delete')
# @login_required
# def card_delete(card_id):
#     card = Card.query.filter_by(id=card_id).first()
#     if card:
#         deck_id = card.deck_id
#         deck = Deck.query.filter_by(id=deck_id).first()
#         deck.deck_score=0
#         cards = Card.query.filter_by(deck_id=deck.id).all()
#         for el in cards:
#             el.review=0
#         db.session.add(deck)
#         db.session.delete(card)
#         db.session.commit()
#         return redirect(url_for('.deck_update', deck_id=deck_id)) 
#     return render_template('404.html')

# @app.route('/card/<int:card_id>/edit', methods = ['GET','POST'])
# @login_required
# def card_edit(card_id):
#     card = Card.query.filter_by(id=card_id).first()
#     deck_id = card.deck_id
#     if request.method =='POST':
#         front = request.form['front']
#         back = request.form['back']
#         card.front = front
#         card.back=back
#         db.session.add(card)
#         db.session.commit()
#         return redirect(url_for('.deck_update', deck_id=deck_id))
#     return render_template('cardupdate.html', card=card)

# @app.route('/deck/<int:deck_id>/reset')
# @login_required
# def deck_reset(deck_id):
#     deck = Deck.query.filter_by(id=deck_id).first()
#     deck.deck_score=0
    
#     cards = Card.query.filter_by(deck_id=deck.id).all()
#     if cards:
#         for card in cards:
#             card.review=0
#             db.session.add(card)
#     db.session.add(deck)
#     db.session.commit()
#     return redirect('/')
    



