from service.model import db
from service.models.baseModel import BaseModel

# 刷题状态表
class UserProblemSetLogModel(db.Model,BaseModel):
    __tablename__ = 'UserProblemSetLog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    set_id = db.Column(db.Integer)
    # 操作类型，1-创建题单，2-加入题单，3-添加题目，4-删除题目，0-删除题单
    op_type = db.Column(db.Integer)
    problem_id = db.Column(db.Integer)
    update_time = db.Column(db.DateTime,default=None)
