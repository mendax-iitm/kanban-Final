from application.workers import celery
from celery.schedules import crontab
from datetime import datetime
from application.models import User, List, Card
from base64 import b64encode
from application.email import send_email
from jinja2 import Template
from application.helperfunction import monthlyProgress
from application import config
from flask import current_app as app
import os
from weasyprint import HTML
import uuid
import matplotlib.pyplot as plt
from PIL import Image



@celery.task()
def print_current_time_job():
    print("START")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string) 
    print("COMPLETE")
    return dt_string

@celery.task()
def just_say_hello(name):
    print("INSIDE TASK")
    print('Hello {}'.format(name))

@celery.task()
def dailyReminders():
    users=User.query.all()
    print(users)
    for user in users:
        msg='You have no task left. Enjoy your day'
        lists = List.query.filter_by(user_id=user.user_id).all()
        incomplete=0
        for list in lists:
            cards = Card.query.filter_by(list_id=list.id).all()
            for card in cards:
                if int(card.deadline_days)>=-1 and card.completed==0:
                    incomplete+=1
        if incomplete>0:
            msg='You have '+str(incomplete)+' tasks left. Kindly do as soon as possible'
        send_email(user.email,'Status update for Kanban',
        '''
        Hello {0},
        {1},
        Thank you for using Kanban
        '''.format(user.username,msg))

@celery.task()
def monthlyReview():
    users=User.query.all()
    for user in users:
        id=user.user_id
        cards_created, completed, incomplete, deadline_passed =monthlyProgress(id)
        
        template_file=open("thank-you.html")
        print(template_file)
        TEMPLATE=template_file.read()
        template_file.close()
        template=Template(TEMPLATE) 
        image_labels=['To be completed','Completed', 'Deadline Passed']
        image_data=[incomplete,completed,deadline_passed]
        plt.bar(image_labels,height=image_data,color=['yellow','green','red'])
        plt.ylabel('No. of tasks')
        plt.savefig('barchart1.png')
        with open("barchart1.png", "rb") as image_file:
            image_data = image_file.read()
        image_base64 = b64encode(image_data)
        image=Image.open("barchart1.png")
        message=template.render(cards_created=cards_created, completed=completed, incomplete=incomplete, deadline_passed=deadline_passed,username=user.username,image_base64=image_base64)
        send_email(user.email,subject='Monthly Progress Report',message=message,content="html")
@celery.task()
def monthlyPdfReport():
    users=User.query.all()
    for user in users:
        id=user.user_id
        cards_created, completed, incomplete, deadline_passed =monthlyProgress(id)
        
        template_file=open("thank-you.html")
        print(template_file)
        TEMPLATE=template_file.read()
        template_file.close()
        template=Template(TEMPLATE)
        image_labels=['To be completed','Completed', 'Deadline Passed']
        image_data=[incomplete,completed,deadline_passed]
        plt.bar(image_labels,height=image_data,color=['yellow','green','red'])
        plt.ylabel('No. of tasks')
        plt.savefig('barchart1.png')
        with open("barchart1.png", "rb") as image_file:
            image_data = image_file.read()
        image_base64 = b64encode(image_data)
        image=Image.open("barchart1.png") 
        message=template.render(cards_created=cards_created, completed=completed, incomplete=incomplete, deadline_passed=deadline_passed,username=user.username,image_base64=image_base64)
        html=HTML(string=message)
        file_name=str(user.username)+".pdf"
        html.write_pdf(target=file_name)
        send_email(user.email,subject='Monthly Progress Report PDF',message=message,content='html',attachment_file='{0}.pdf'.format(user.username))

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=20), dailyReminders.s(), name='dailyReminders')
    sender.add_periodic_task(crontab(0,0,day_of_month='1',month_of_year='1-12'), monthlyReview.s(), name='monthlyReviews')
    # sender.add_periodic_task(crontab(), monthlyPdfReport.s(), name='monthlyPDFReport')
    sender.add_periodic_task(crontab(0,0,day_of_month='1',month_of_year='1-12'), monthlyPdfReport.s(), name='monthlyPdfReport')