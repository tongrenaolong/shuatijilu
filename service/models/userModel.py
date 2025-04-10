from service.model import db
from service.models.baseModel import BaseModel

# 用户表
class UserModel(db.Model,BaseModel):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100))
    password = db.Column(db.String(255))
    username = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.user_id},{self.account},{self.username},{self.password},{self.created_at}>'