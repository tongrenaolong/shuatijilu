from service.model import db
from service.models.baseModel import BaseModel

# 用户表
class UserOperationLogModel(db.Model,BaseModel):
    __tablename__ = 'UserOperationLog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_permission = db.Column(db.Integer) # 0-普通用户，1-系统管理员
    ip = db.Column(db.String(100))
    url = db.Column(db.String(100))
    method = db.Column(db.String(100))
    user_agent = db.Column(db.String(100))
    update_time = db.Column(db.DateTime)