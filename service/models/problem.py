from service.model import db
from service.models.baseModel import BaseModel
# 题目表
class Problem(db.Model, BaseModel):
    __tablename__ = 'problems'

    id = db.Column(db.Integer, primary_key=True)
    problem_name = db.Column(db.String(100))
    link = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    difficulty = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Problem(id={self.id}, name={self.problem_name}, difficulty={self.difficulty})>'