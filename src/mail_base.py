#!/usr/bin/python
import smtplib, logging
import sys
from email.mime.text import MIMEText
import email.mime.multipart
import email.mime.text
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

'''
Example:
host = "smtp.exmail.qq.com"
user = "10000@qq.com"   # who send the email
pass = "123456789a0123" # the password for user
postfix = "qq.com"
recv_list = ['1234@qq.com', '1234@163.com']  # who will recv the email
'''
class mail_base(object):
    def __init__(self, host, user, password, postfix, recv_list):
        self.mail_host = host
        self.mail_user = user
        self.mail_pass = password
        self.mail_postfix = postfix
        self.recv_list = recv_list

    def reset_recv_list(self, recv_list):
        self.recv_list = recv_list

    # send the email that only has text
    def send_text(self, subject, content):
        me = self.mail_user
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ';'.join(self.recv_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, self.recv_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            logging.error(str(e))
            return False

    # send the email that has images
    # images will show after text content.
    def send_image(self, subject, content, img_set=None):
        me = self.mail_user
        msg_root = MIMEMultipart('related')

        if img_set:
            for index, img in enumerate(img_set):
                fp = open(img, 'rb')
                msg_image = MIMEImage(fp.read())
                fp.close()
                msg_image.add_header('Content-ID', '<image%d>' % (index + 1))
                msg_root.attach(msg_image)
                content += '<p><img src = "cid:image%d"></p>' % (index + 1)

        msg = MIMEText(content, 'html', 'utf-8')
        msg_root['Subject'] = subject
        msg_root['From'] = me
        msg_root['To'] = ';'.join(self.recv_list)
        msg_root.attach(msg)

        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, self.recv_list, msg_root.as_string())
            server.close()
            return True

        except Exception, e:
            logging.error(str(e))
            return False



