from celery.schedules import crontab
from setting import CELERY_BROKER, CELERY_BACKEND

broker_url = CELERY_BROKER
result_backend = CELERY_BACKEND

# Celery 配置
broker_connection_retry_on_startup = True
broker_connection_max_retries = 10
broker_connection_timeout = 30
broker_transport_options = {
    'visibility_timeout': 3600,
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
}

# 定时任务配置
beat_schedule = {
    'daily-review-plan': {
        'task': 'create_review_plan',
        'schedule': crontab(hour=3),  # 每天凌晨 3:00 执行
    },
    'daily-send-email': {
        'task': 'send_review_plan_email',
        'schedule': crontab(hour=8),  # 每天早上 8:00 执行
    },
    'auth-code-reminder': {
        'task': 'send_auth_code_reminder',
        'schedule': timedelta(days=180),  # 每180天执行一次
    }
}