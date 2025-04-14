import os
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import markdown2
from service.models.sendEmailLogModel import SendEmailLogModel
from service.models.userModel import UserModel
from service.utils.fun import get_datetime
from setting import AUTHORIZATION_CODE,EMAIL_ADDR,SMTP_SERVER,SMTP_PORT

class EmailRPC(object):
    @classmethod
    def send_auth_code_reminder(cls):
        admin_email = '18706838263@163.com'
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = formataddr((Header('系统提醒', 'utf-8').encode(), EMAIL_ADDR))
            msg['To'] = formataddr((Header('管理员', 'utf-8').encode(), admin_email))
            msg['Subject'] = Header('OnlineRecord邮箱授权码到期提醒', 'utf-8')

            # 邮件正文
            content = """
            <html>
            <body>
                <h3>系统提醒</h3>
                <p>OnlineRecord 项目 163邮箱 授权码即将到期，请及时续约。</p>
                <p>请登录邮箱重新生成授权码并更新系统配置。</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(content, 'html', 'utf-8'))

            # 发送邮件
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(EMAIL_ADDR, AUTHORIZATION_CODE)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"发送授权码到期提醒邮件失败: {str(e)}")
            return False

    @classmethod
    def send_review_plan_email(cls):
        try:
            from service.server import Server
            app = Server.get_app()
            with app.app_context():
                # 获取所有用户
                users = UserModel.all()
                
                # 获取当前日期的报告目录
                current_date = datetime.now().strftime("%Y-%m-%d")
                report_dir = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    'review_plan',
                    current_date
                )
                
                if not os.path.exists(report_dir):
                    print(f"No reports found for date: {current_date}")
                    return False
                
                for user in users:
                    # 构建报告文件路径
                    report_path = os.path.join(report_dir, f'user_{user["id"]}_{current_date}.md')
                    
                    if not os.path.exists(report_path):
                        continue
                    
                    # 读取报告内容并转换为HTML
                    with open(report_path, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                    # 转换Markdown为HTML
                    html_content = markdown2.markdown(report_content, extras=['tables', 'fenced-code-blocks'])
                    
                    # 添加CSS样式
                    styled_html = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                            h1 {{ color: #2c3e50; }}
                            h2 {{ color: #34495e; }}
                            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                            th {{ background-color: #f5f5f5; }}
                            code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; }}
                            pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }}
                        </style>
                    </head>
                    <body>
                        {html_content}
                    </body>
                    </html>
                    """
                    
                    # 创建邮件
                    msg = MIMEMultipart('alternative')
                    msg['From'] = formataddr((Header('刷题助手', 'utf-8').encode(), EMAIL_ADDR))
                    msg['To'] = formataddr((Header(user['username'], 'utf-8').encode(), user['email']))
                    msg['Subject'] = Header(f"{current_date} 刷题分析报告", 'utf-8')
                    
                    # 添加纯文本和HTML两种格式
                    msg.attach(MIMEText(report_content, 'plain', 'utf-8'))
                    msg.attach(MIMEText(styled_html, 'html', 'utf-8'))
                    
                    try:
                        # 发送邮件
                        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                            server.login(EMAIL_ADDR, AUTHORIZATION_CODE)
                            server.send_message(msg)
                        
                        # 记录发送成功日志
                        log_data = {
                            'user_id': user['id'],
                            'email': user['email'],
                            'update_time': get_datetime(),
                            'status': 1  # 发送成功
                        }
                        SendEmailLogModel.add_new(log_data)
                        print(f"Email sent successfully to {user['account']}")
                    except Exception as e:
                        # 记录发送失败日志
                        log_data = {
                            'user_id': user['id'],
                            'email': user['email'],
                            'update_time': get_datetime(),
                            'status': 2  # 发送失败
                        }
                        SendEmailLogModel.add_new(log_data)
                        print(f"Failed to send email to {user['account']}: {str(e)}")
            return True
        except Exception as e:
            print(f"Error in send_review_plan_email: {str(e)}")
            return False