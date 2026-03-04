"""
SMTP Sender - SMTP邮件发送
支持163、QQ等邮箱服务商
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict


class SMTPSender:
    """SMTP邮件发送"""

    def __init__(self, host: str, port: int, username: str, password: str):
        """
        初始化

        Args:
            host: SMTP服务器地址
            port: SMTP端口
            username: 邮箱账号
            password: 邮箱密码/授权码
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send_email(
        self,
        to: str | list,
        subject: str,
        html_content: str,
        from_email: str = None
    ) -> Dict:
        """
        发送邮件

        Args:
            to: 收件人邮箱（字符串或列表）
            subject: 邮件标题
            html_content: HTML内容
            from_email: 发件人邮箱（可选，默认使用username）

        Returns:
            {"success": bool, "message": str, "id": str}
        """
        # 统一转换为列表
        if isinstance(to, str):
            recipients = [to]
        else:
            recipients = to

        if not recipients:
            return {"success": False, "message": "收件人邮箱为空", "id": None}

        from_email = from_email or self.username

        try:
            print(f"📧 正在通过SMTP发送邮件到: {len(recipients)} 个收件人")
            print(f"   SMTP服务器: {self.host}:{self.port}")
            for recipient in recipients:
                print(f"   - {recipient}")

            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = ', '.join(recipients)

            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # 连接SMTP服务器
            if self.port == 465:
                # SSL连接
                server = smtplib.SMTP_SSL(self.host, self.port, timeout=30)
            else:
                # TLS连接
                server = smtplib.SMTP(self.host, self.port, timeout=30)
                server.starttls()

            # 登录
            server.login(self.username, self.password)

            # 发送给所有收件人
            server.send_message(msg)
            server.quit()

            print(f"✅ 邮件发送成功!")

            return {
                "success": True,
                "message": f"邮件发送成功到 {len(recipients)} 个收件人",
                "id": "smtp_sent"
            }

        except smtplib.SMTPAuthenticationError:
            error_msg = "SMTP认证失败，请检查邮箱密码或授权码"
            print(f"❌ {error_msg}")
            return {"success": False, "message": error_msg, "id": None}

        except smtplib.SMTPException as e:
            error_msg = f"SMTP错误: {str(e)}"
            print(f"❌ {error_msg}")
            return {"success": False, "message": error_msg, "id": None}

        except Exception as e:
            error_msg = str(e)
            print(f"❌ 邮件发送失败: {error_msg}")
            return {"success": False, "message": error_msg, "id": None}


def send_email(
    host: str,
    port: int,
    username: str,
    password: str,
    to: str,
    subject: str,
    html_content: str,
    from_email: str = None
) -> Dict:
    """便捷函数：发送邮件"""
    sender = SMTPSender(host, port, username, password)
    return sender.send_email(to, subject, html_content, from_email)
