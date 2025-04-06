from service.model import db
from baseModel import BaseModel

# 订阅表
class UserSubscriptions(db.Model,BaseModel):
    __tablename__ = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)
    authority = db.Column(db.Boolean)

    def __repr__(self):
        return f'<UserSubscription(user_id={self.user_id}, set_id={self.set_id})>'