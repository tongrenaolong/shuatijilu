from service.model import db
from service.models.baseModel import BaseModel

# 订阅表
class UserSubscriptionsModel(db.Model,BaseModel):
    __tablename__ = 'UserSubscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)
    authority = db.Column(db.Integer)

    def __repr__(self):
        return f'<UserSubscription(user_id={self.user_id}, set_id={self.set_id})>'