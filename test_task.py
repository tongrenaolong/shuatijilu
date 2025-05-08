from celery import Celery
from service.rpc.ai_rpc import AiRPCService
from service.rpc.email_rpc import EmailRPC

app = Celery('task')
app.config_from_object('service.back_work.celery_config')

AiRPCService.create_review_plan()

EmailRPC.send_review_plan_email()
