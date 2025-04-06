from service.model import db
from baseModel import BaseModel

# 题单表
class ProblemSets(db.Model,BaseModel):
    __tablename__ = 'problem_sets'

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer)
    set_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<ProblemSet(id={self.id}, name={self.set_name})>'