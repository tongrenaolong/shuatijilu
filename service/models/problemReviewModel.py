from service.model import db
from service.models.baseModel import BaseModel

class ProblemReviewModel(db.Model, BaseModel):
    """每日复习题目表"""
    __tablename__ = 'ProblemReview'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    problem_set_id = db.Column(db.Integer, nullable=True, index=True)
    problem_id = db.Column(db.Integer, nullable=True, index=True)
    user_id = db.Column(db.Integer, nullable=True, index=True)
    create_time = db.Column(db.DateTime, nullable=True, index=True)
    status = db.Column(db.Integer, default=0, nullable=True)