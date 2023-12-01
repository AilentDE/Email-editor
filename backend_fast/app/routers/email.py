from fastapi import APIRouter, Depends, Body, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import BaseModel, EmailStr
from ..dependencies import QueryParams
from .files import get_mongo_file
import smtplib
from email.mime.text import MIMEText
import os

router = APIRouter(
    prefix="/email",
    tags=["email"]
)

class DbQuery(BaseModel):
    skip: Union[int, None] = 0
    limit: Union[int, None] = 100

class MailRequest(BaseModel):
    file_id: str
    mail_body: str

def send_mail(target:str, body:str, feature: dict, subject:str = "來自可洛斯的通知"):
    msg = body
    for el in feature.keys():
        msg = msg.replace("{{"+str(el)+"}}", str(feature[el]))
    mail = MIMEText(msg, 'html', 'utf-8')
    mail['Subject'] = subject
    mail['From'] = 'service@clusters.tw'
    mail['To'] = target

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('clusters_info@clusters.tw', os.environ['MAIL_PASS'])
    try:
        status = smtp.sendmail('service@clusters.tw', target, mail.as_string())
    except Exception as error:
        smtp.quit()
        return {
            "success": False,
            "message": '信件寄送失敗了',
            "detail": f'{error}'
        }
    smtp.quit()
    return {
        "success": True,
        "message": '信件寄出成功'
    }

@router.post("/send-sample-email", responses={
    200: {
        "content": {
            "application/json": {
                "message": "Sample letter has been sent out."
            }
        }
    }
})
async def send_sample_email(commons: DbQuery, mail_request : MailRequest, email: EmailStr = Body()):
    # mail_request : MailRequest = Body(embed=True), email: str = Body()
    feature = get_mongo_file(mail_request.file_id, commons)[0]
    if feature['subject']:
        subject = feature['subject']
    else:
        subject = None
    return send_mail(email, mail_request.mail_body, feature, subject)

@router.post("/send-emails")
async def send_emails(background_tasks: BackgroundTasks, mail_request : MailRequest = Body(embed=True)):
    feature =  get_mongo_file(mail_request.file_id, None)
    for tar in feature:
        print(f"發信給{tar['email']}")
        if tar['subject']:
            subject = tar['subject']
        else:
            subject = None
        background_tasks.add_task(send_mail, tar['email'], mail_request.mail_body, tar, subject)
    return {
        "success": True,
        "message": "所有信件已安排送出"
    }