import os
from celery import Celery
from setting import CELERY_BROKER, CELERY_BACKEND
from service.models.userModel import UserModel
from service.models.userSubscriptionModel import UserSubscriptionModel
from service.models.userProblemLogModel import UserProblemLogModel
from openai import OpenAI
from datetime import datetime, timedelta

broker = CELERY_BROKER
backend = CELERY_BACKEND
# broker = 'redis://47.94.156.51:6379/0'
# backend = 'redis://47.94.156.51:6379/0'
app = Celery('task', broker=broker, backend=backend)

AI_API_KEY = "sk-0e214e7c2b53428e99ca96c456f0ff68"
AI_URL = "https://api.deepseek.com"
client = OpenAI(api_key=AI_API_KEY, base_url=AI_URL)


@app.task(name='add')
async def add():
    return 1+1

@app.task(name='create_review_plan')
async def create_review_plan():
    try:
        # 获取所有用户
        users = UserModel.all()
        print(f'users: {users}')
        
        # 创建输出目录
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports')
        os.makedirs(output_dir, exist_ok=True)
        
        for user in users:
            print('-')
            # 获取用户订阅的题集
            subscriptions = UserSubscriptionModel.get_where(
                conditions={'user_id': user['id']}
            )
            
            if not subscriptions:
                continue
                
            user_analysis = f"# {user['username']} 的刷题分析报告\n\n"
            user_analysis += f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for subscription in subscriptions:
                # 获取该用户在这个题集的刷题记录
                problem_logs = UserProblemLogModel.get_where(
                    conditions={
                        'user_id': user['id'],
                        'set_id': subscription['set_id']
                    }
                )
                
                if not problem_logs:
                    continue
                
                # 准备AI分析的数据
                analysis_text = f"用户在题集{subscription['set_id']}中的刷题记录如下：\n"
                for log in problem_logs:
                    analysis_text += f"- 题目ID：{log['problem_id']}\n"
                    analysis_text += f"- 描述：{log['description']}\n"
                    analysis_text += f"- 更新时间：{log['update_time']}\n\n"
                
                # 调用AI进行分析
                prompt = f"""
                请分析以下刷题记录，并给出建议：
                {analysis_text}
                请从以下几个方面进行分析：
                1. 刷题频率和规律
                2. 题目难度分布
                3. 学习建议和改进方向
                """
                
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个专业的编程教育顾问"},
                        {"role": "user", "content": prompt},
                    ],
                    stream=False
                )
                
                ai_analysis = response.choices[0].message.content
                user_analysis += f"\n## 题集 {subscription['set_id']} 分析\n\n"
                user_analysis += ai_analysis + "\n\n"
            
            # 保存分析报告
            report_path = os.path.join(output_dir, f'user_{user["id"]}_analysis.md')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(user_analysis)
        
        return True
    except Exception as e:
        print(f"Error in create_review_plan: {str(e)}")
        return False

# 测试代码
if __name__ == "__main__":
    create_review_plan()
