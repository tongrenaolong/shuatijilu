from service.model import db
from service.models.baseModel import BaseModel

# 刷题状态表
class UserProblemStatusModel(db.Model,BaseModel):
    __tablename__ = 'UserProblemStats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    problem_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    time_spent = db.Column(db.Integer)  # time in seconds
    description = db.Column(db.Text)
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<UserProblemStatus {self.user_id},{self.problem_id},{self.status},{self.time_spent},{self.description}>'