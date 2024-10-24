import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, Depends, BackgroundTasks
from starlette.requests import Request

from apps.utils.authentication import get_current_user
from config import templates
from config import conf

user_router = APIRouter()


@user_router.get("/profile", name='user_profile')
async def user_profile(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(request, 'apps/users/profile.html')


def send_email_smtp(recipient_email: str, subject: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = conf.smtp.EMAIL_HOST
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP(conf.smtp.EMAIL_HOST, conf.smtp.EMAIL_PORT) as server:
        server.starttls()
        server.login(conf.smtp.EMAIL_HOST_USER, conf.smtp.EMAIL_HOST_PASSWORD)
        server.sendmail(conf.smtp.EMAIL_HOST_USER, recipient_email, msg.as_string())


@user_router.get("/send-email/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_smtp, email, "Notification", "Hello")
    return {"message": "Notification sent in the background"}
