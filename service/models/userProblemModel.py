from service.model import db
from service.models.baseModel import BaseModel

# 刷题状态表
class UserProblemModel(db.Model,BaseModel):
    __tablename__ = 'UserProblem'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)
    problem_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    description = db.Column(db.Text)
    image = db.Column(db.LargeBinary)
    update_time = db.Column(db.DateTime)