import os
import httpx
from celery import Celery
from service.models.problemModel import ProblemModel
from setting import CELERY_BROKER, CELERY_BACKEND
from service.models.userModel import UserModel
from service.models.userSubscriptionModel import UserSubscriptionModel
from service.models.userProblemLogModel import UserProblemLogModel
from datetime import datetime
from service.server import Server
from celery.schedules import crontab
from service.rpc.ai_rpc import AiRPCService
from service.rpc.email_rpc import EmailRPC

app = Celery(
    'task', 
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=10,
    broker_connection_timeout=30,
    broker_transport_options={
        'visibility_timeout': 3600,
        'socket_timeout': 30,
        'socket_connect_timeout': 30,
    }
)
# 添加定时任务配置
app.conf.beat_schedule = {
    'daily-review-plan': {
        'task': 'create_review_plan',
        'schedule': crontab(hour=3),  # 每天早上 8:00 执行
    },
    'daily-send-email': {
        'task': 'send_review_plan_email',
        'schedule': crontab(hour=8),  # 每天早上 8:00 执行
    },
}

@app.task(name='create_review_plan')
def create_review_plan():
    AiRPCService.create_review_plan()

@app.task(name='send_review_plan_email')
def send_review_plan_email():
    EmailRPC.send_review_plan_email()