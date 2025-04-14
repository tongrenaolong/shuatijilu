# Please install OpenAI SDK first: `pip3 install openai`
import os
from datetime import datetime
import httpx
from openai import OpenAI
from service.models.problemModel import ProblemModel
from service.models.userModel import UserModel
from service.models.userProblemLogModel import UserProblemLogModel
from service.models.userSubscriptionModel import UserSubscriptionModel
from setting import AI_API_KEY,AI_URL

class AiRPCService():
    client = OpenAI(
        api_key=AI_API_KEY,
        base_url=AI_URL,
        http_client=httpx.Client(verify=False)  # 测试关闭 SSL 验证
    )
    @classmethod
    def create_review_plan(cls):
        try:
            from service.server import Server
            app = Server.get_app()
            with app.app_context():
                users = UserModel.all()

                # 创建输出目录
                current_date = datetime.now().strftime("%Y-%m-%d")
                output_dir = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                    'review_plan', 
                    current_date
                )
                os.makedirs(output_dir, exist_ok=True)

                for user in users:
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
                        problem_list = ProblemModel.get_where(
                            conditions={
                                'set_id': subscription['set_id']
                            },
                            key='id'
                        )

                        # 准备AI分析的数据
                        analysis_text = f"用户在题集{subscription['set_id']}中的刷题记录如下：\n"
                        for log in problem_logs:
                            analysis_text += f"- 题目ID：{log['problem_id']}\n"
                            analysis_text += f"- 题目名：{problem_list[log['problem_id']]['problem_name']}\n"
                            analysis_text += f"- 题目链接：{problem_list[log['problem_id']]['link']}\n"
                            difficulty = ['Easy', 'Medium', 'Hard']
                            analysis_text += f"- 题目难度：{difficulty[problem_list[log['problem_id']]['difficulty']]}\n"
                            analysis_text += f"- 更新时间：{log['update_time']}\n\n"

                        # 调用AI进行分析
                        prompt = f"""
                        请分析以下刷题记录，并给出建议：
                        {analysis_text}
                        
                        请从以下几个方面进行分析：
                        1. 刷题频率和规律
                        2. 题目难度分布
                        3. 学习建议和改进方向
                        4. 今日复习计划：
                           - 请根据艾宾浩斯遗忘曲线，使用表格的方式列出今天({datetime.now().strftime('%Y-%m-%d')})需要复习的题目
                           - 对于每道题目，给出：题目名称、难度、原始链接
                           - 建议复习的顺序和每道题目的重点内容
                        """
                        obj = cls()
                        response = obj.client.chat.completions.create(
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
                    timestamp = datetime.now().strftime("%Y-%m-%d")  # 用下划线替代冒号
                    report_path = os.path.join(output_dir, f'user_{user["id"]}_{timestamp}.md')
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(user_analysis)

            return True
        except Exception as e:
            print(f"Error in create_review_plan: {str(e)}")
            return False