from service.back_work.tasks import create_review_plan,add
from service.handler.baseHandler import BaseHandler
import asyncio

class TestTask(BaseHandler):
    @classmethod
    def test_task(cls):
        obj = cls()
        # result = asyncio.run(create_review_plan())
        task = create_review_plan.delay()
        return obj.r(msg="任务已提交", data={"task_id": task.id}, code=200)
        # result = asyncio.run(add())
        # return obj.r(msg="任务已提交",data=result, code=200)