from service.model import db
from service.models.baseModel import BaseModel

class ProblemRelationModel(db.Model, BaseModel):
    """题目间关系，是否是同类型"""
    __tablename__ = 'ProblemRelation'

    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, nullable=True)
    target_problem_id = db.Column(db.Integer, nullable=True)
    relation = db.Column(db.Integer, default=0, nullable=True)