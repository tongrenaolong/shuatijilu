from service.model import db
from service.models.baseModel import BaseModel

# 用户表
class UserModel(db.Model,BaseModel):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100))
    password = db.Column(db.String(255))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)