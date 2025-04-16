from celery import Celery
from service.rpc.ai_rpc import AiRPCService
from service.rpc.email_rpc import EmailRPC

app = Celery('task')
app.config_from_object('service.back_work.celery_config')

@app.task(name='create_review_plan')
def create_review_plan():
    AiRPCService.create_review_plan()

@app.task(name='send_review_plan_email')
def send_review_plan_email():
    EmailRPC.send_review_plan_email()

@app.task(name='send_auth_code_reminder')
def send_auth_code_reminder():
    EmailRPC.send_auth_code_reminder()