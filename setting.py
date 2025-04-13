# -*- coding: utf-8 -*-
"""load .env and so on, default setting"""
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv(override=True)
ROOT = os.path.dirname(os.path.abspath(__file__))

# set default set
DATABASE_HOST = os.getenv("DATABASE_HOST", None)
DATABASE_USER = os.getenv("DATABASE_USER", None)
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", None)
DATABASE_NAME = os.getenv("DATABASE_NAME", None)
# --------databases-----------
MYSQL_URL = 'mysql+pymysql://' + \
    str(DATABASE_USER) + ':' + quote(str(DATABASE_PASSWORD))+'@' + \
    str(DATABASE_HOST)+':'+str(DATABASE_PORT)+'/'+str(DATABASE_NAME)

SQLALCHEMY_ENABLE_POOL_PRE_PING = os.getenv(
    "SQLALCHEMY_ENABLE_POOL_PRE_PING", None)
SQLALCHEMY_DISABLE_POOL = os.getenv("SQLALCHEMY_DISABLE_POOL", None)

SERVER_HOST = os.getenv("SERVER_IP", "0.0.0.0")
SERVER_PORT = os.getenv("SERVER_PORT", "5000")
LOG_DIR = os.getenv("LOG_DIR", "")
if "" == LOG_DIR:
    LOG_DIR = ROOT + "/log"
URL_DEFAULT_PREFIX = os.getenv("URL_DEFAULT_PREFIX", "").strip("/")
DEBUG = os.getenv("DEBUG", "")
CELERY_BROKER = os.getenv("CELERY_BROKER", "")
CELERY_BACKEND = os.getenv("CELERY_BACKEND", "")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_URL = os.getenv("AI_URL", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = os.getenv("SMTP_PORT", 465)
EMAIL_ADDR = os.getenv("EMAIL_ADDR", "")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE", "") # 授权码