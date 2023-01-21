
import smtplib
from application import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER_HOST= "localhost"
SMTP_SERVER__PORT= 1025
SENDER_ADDRESS= "email@abhishek.com"
SENDER_PASSWORD= ""

def send_email(to_address,subject,message,content='text',attachment_file=None):
    msg=MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address
    msg['Subject']=subject
    if content=='html':
        msg.attach(MIMEText(message,"html"))
    else:
        msg.attach(MIMEText(message,"plain"))
    if attachment_file:
        with open(attachment_file, 'rb') as attachment:
            part=MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment_file}",)
        msg.attach(part)

    try:
        s= smtplib.SMTP(host=SMTP_SERVER_HOST,
                        port=SMTP_SERVER__PORT)
        s.login(SENDER_ADDRESS,SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
    except:
        return False
    return True