from service.model import db
from service.models.baseModel import BaseModel
# 题目表
class ProblemTypeModel(db.Model, BaseModel):
    __tablename__ = 'ProblemType'

    id = db.Column(db.Integer, primary_key=True)
    type_level = db.Column(db.Integer)
    type_name = db.Column(db.String(100)) # 唯一键
    parent_type_id = db.Column(db.Integer)