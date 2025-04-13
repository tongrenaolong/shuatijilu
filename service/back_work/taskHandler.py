from service.back_work.tasks import create_review_plan
from service.handler.baseHandler import BaseHandler
import asyncio

class TestTask(BaseHandler):
    @classmethod
    def test_task(cls):
        obj = cls()
        task = create_review_plan.delay()
        return obj.r(msg="任务已提交", data={"task_id": task.id}, code=200)

    @classmethod
    def send_review_plan_email(cls):
        obj = cls()
        task = create_review_plan.delay()
        return obj.r(msg="任务已提交", data={"task_id": task.id}, code=200)
