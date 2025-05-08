import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr  # 新增关键工具函数

# 配置信息
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465  # SSL端口
EMAIL_ADDR = "18706838263@163.com"
PASSWORD = "FCVFB34uyMA4qpFG"  # 授权码
TO_ADDR = "3300763927@qq.com"


def send_email_via_smtp():
    # 创建邮件内容
    msg = MIMEMultipart()

    # 修正点1：使用formataddr规范From/To头格式
    msg['From'] = formataddr((
        Header('发件人名称', 'utf-8').encode(),  # 编码中文
        EMAIL_ADDR
    ))
    msg['To'] = formataddr((
        Header('收件人名称', 'utf-8').encode(),
        TO_ADDR
    ))
    msg['Subject'] = Header("Python邮件测试", 'utf-8')

    # 邮件正文
    body = """
    <h1>这是一封测试邮件</h1>
    <p>来自Python程序的163邮箱发送测试</p>
    <p>发送时间：{}</p>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 修正点2：明确指定邮件内容类型
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        # 建立安全连接
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDR, PASSWORD)

            # 修正点3：使用send_message替代sendmail
            server.send_message(msg)

        print("邮件发送成功！")
    except smtplib.SMTPException as e:
        print(f"SMTP协议错误: {str(e)}")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")


# 调用函数
send_email_via_smtp()