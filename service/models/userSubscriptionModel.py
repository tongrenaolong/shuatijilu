from service.model import db
from service.models.baseModel import BaseModel

# 订阅表
class UserSubscriptionModel(db.Model,BaseModel):
    __tablename__ = 'UserSubscription'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)
    authority = db.Column(db.Integer)