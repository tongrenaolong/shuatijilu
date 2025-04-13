
from service.model import db
from service.models.baseModel import BaseModel

# 发送邮件日志表
class SendEmailLogModel(db.Model,BaseModel):
    __tablename__ = 'SendEmailLog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    email = db.Column(db.String(100))
    update_time = db.Column(db.DateTime)
    status = db.Column(db.Integer) # 0-未发送，1-发送成功，2-发送失败