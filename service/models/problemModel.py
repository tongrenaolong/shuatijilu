from service.model import db
from service.models.baseModel import BaseModel
# 题目表
class ProblemModel(db.Model, BaseModel):
    __tablename__ = 'Problem'

    id = db.Column(db.Integer, primary_key=True)
    problem_name = db.Column(db.String(100))
    link = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    difficulty = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)
    type_id = db.Column(db.Integer)