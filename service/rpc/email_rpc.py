from setting import AUTHORIZATION_CODE,EMAIL_ADDR,SMTP_SERVER,SMTP_PORT

class EmailRPC(object):
    @classmethod
    def send_review_plan_email(cls):
        try:
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
                
                # 读取报告内容
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_content = f.read()
                
                # 创建邮件
                msg = MIMEMultipart()
                msg['From'] = formataddr((Header('刷题助手', 'utf-8').encode(), EMAIL_ADDR))
                msg['To'] = formataddr((Header(user['username'], 'utf-8').encode(), user['email']))
                msg['Subject'] = Header(f"{current_date} 刷题分析报告", 'utf-8')
                
                # 邮件正文
                msg.attach(MIMEText(report_content, 'markdown', 'utf-8'))
                
                try:
                    # 发送邮件
                    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                        server.login(EMAIL_ADDR, PASSWORD)
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