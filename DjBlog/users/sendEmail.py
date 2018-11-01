import os
import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class EmailSender(object):

    def __init__(self, to_email):
        # 验证码由六位随机数组成，生成验证码
        ch = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.__verification_code = ''
        for i in range(6):
            self.__verification_code += random.choice(ch)
        # print(verification_code)

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjBlog.settings")
        self.subject = "您好，欢迎注册DjBlog，这是邮箱验证确认邮件，请验证您的验证码"
        self.content = " 您好，欢迎您注册DjBlog，您的验证码是" + self.__verification_code + ",验证码有效期为15分钟"
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.to_emails = [to_email]
        # self.send_emails(subject, content, from_email, to_emails)

    # subject 主题 content 内容 to_email 是一个列表，发送给谁们
    def send_emails(self):
        msg = EmailMultiAlternatives(self.subject, self.content, self.from_email, self.to_emails)
        msg.content_subtype = 'html'
        # 添加附件（可选）
        # msg.attach_file('./test.py')
        # 发送
        msg.send()
        print("send finish")

    #     设置一个获取验证码的方法
    def get_verification_code(self):
        return self.__verification_code

# test = SendEmail('ff603@sina.com')
