from datetime import datetime
import pytz
from application.models import User,List, Card
from application.database import db
from main import cache
# get the standard UTC time 
UTC = pytz.utc

# it will get the time zone 
# of the specified location
IST = pytz.timezone('Asia/Kolkata')
  
# print the date and time in
# standard format
# print("UTC in Default Format : ", 
#       datetime.now(UTC))
  
# print("IST in Default Format : ", 
#       datetime.now(IST))
  
# # print the date and time in 
# # specified format
# datetime_utc = datetime.now(UTC)
# print("Date & Time in UTC : ",
#       datetime_utc.strftime('%Y:%m:%d %H:%M:%S %Z %z'))
  
# datetime_ist = datetime.now(IST)
# print("Date & Time in IST : ", 
#       datetime_ist.strftime('%d:%m:%Y-%H:%M:%S'))
# datetimeist = datetime_ist.strftime('%d:%m:%Y-%H:%M:%S')


# def timeconversion(UTC_datetime):
#     UTC_datetime_timestamp = float(UTC_datetime.strftime("%s"))
#     local_datetime_converted = datetime.fromtimestamp(UTC_datetime_timestamp)
#     return local_datetime_converted

# def totalsecs(local_time):
#     local_time_string = local_time.split()[1]
#     local_time_li = local_time_string.split(':')
#     total = local_time_li[0]*3600+local_time_li[1]*60+local_time_li[2]
#     return total
    
# def secdiff(before_datetime):
#     local_now = timeconversion(datetime.utcnow())
#     total_now = totalsecs(local_now)
#     total_before = totalsecs(before_datetime)
    
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(IST)
    datetime_ist = IST.normalize(local_dt)
    return datetime_ist.strftime('%d:%m:%Y-%H:%M:%S')
def userExist(username):
    user = db.session.query(User).filter(User.username==username).first()
    if user == None:
        return False
    else:
        return True


def find_all_list(user_id):
    return List.query.filter_by(user_id=user_id).all()

@cache.memoize(30)
def find_user(username):
    return User.query.filter_by(username=username).first()

def emailExist(email):
    user = db.session.query(User).filter(User.email==email).first()
    if user == None:
        return False
    else:
        return True
    
def monthlyProgress(user_id):
    lists = List.query.filter_by(user_id=user_id).all()
    cards_created=0
    deadline_passed=0
    incomplete=0
    completed=0
    for list in lists:
        cards = Card.query.filter_by(list_id=list.id).all()
        today = datetime.today()
        for card in cards:
            if (today-card.created_time).days<=30:
                cards_created += 1
            if card.completed==1 and (today-card.completed_time).days<=30:
                completed += 1
            elif card.deadline_days>=-1:
                incomplete += 1
            elif (today-card.deadline).days<=30 and card.completed==0:
                deadline_passed += 1
    return cards_created, completed, incomplete, deadline_passed



