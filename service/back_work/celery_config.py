from celery.schedules import crontab
from datetime import timedelta
from setting import CELERY_BROKER, CELERY_BACKEND

# 基础配置
broker_url = CELERY_BROKER
result_backend = CELERY_BACKEND
timezone = 'Asia/Shanghai'
enable_utc = False

# 连接配置
broker_connection_retry_on_startup = True
broker_connection_max_retries = 10
broker_connection_timeout = 30

# 传输选项
broker_transport_options = {
    'visibility_timeout': 3600,  # 1小时可见性超时
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'max_retries': 3,  # 消息传输重试次数
}

# 定时任务配置
beat_schedule = {
    'daily-review-plan': {
        'task': 'create_review_plan',
        'schedule': crontab(hour=3,minute=0),  # 每天凌晨3:00
        'options': {
            'retry': True,
            'retry_policy': {
                'max_retries': 3,
                'interval_start': 60,
            }
        }
    },
    'daily-send-email': {
        'task': 'send_review_plan_email',
        'schedule': crontab(hour=8,minute=0),  # 每天上午9:01
        # 'options': {
        #     'expires': 3600  # 1小时后过期
        # }
    },
    'auth-code-reminder': {
        'task': 'send_auth_code_reminder',
        'schedule': crontab(hour=9, minute=0, day_of_month='1', month_of_year='*/6'),  # 每半年1号9:00
        'args': (180,),  # 传递180天参数
    }
}