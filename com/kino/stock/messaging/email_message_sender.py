"""
发送邮件
"""

import os
import traceback
from datetime import datetime
from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from com.kino.stock.utils.annotation import singleton
from com.kino.stock.messaging.message_sender import MessageSender, MessageInfo


class EmailMessageInfo(MessageInfo):

    def __init__(self, subject, content, to_address=None, profile=None, from_tag=None, file_paths=None,
                 subject_prefix=None):
        self.file_paths = file_paths
        self.to_address = to_address
        super().__init__(subject, content=content, profile=profile, from_tag=from_tag, subject_prefix=subject_prefix)


@singleton(func_name="get_singleton_str")
class EmailMessageSender(MessageSender):

    def __init__(self, server_host, server_port, start_tls, from_password, from_address,
                 same_subject_limit_second=60, logger=None, to_address=None):
        self.server_host = server_host
        self.server_port = server_port
        self.start_tls = start_tls
        self.from_password = from_password
        self.from_address = from_address
        self.to_address = to_address
        super().__init__(logger=logger, same_subject_limit_second=same_subject_limit_second)

    def send(self, message_info):
        server = None
        try:
            to_address = message_info.to_address or self.to_address
            if not to_address:
                return None

            send_time = datetime.now()
            if not self.check_send_limit(send_time, message_info):
                return None

            from_tag = message_info.from_tag or message_info.profile
            content_prefix = '<From: {}; {} {}>'.format(from_tag, message_info.create_time, send_time)
            content = '{}\n{}'.format(content_prefix, message_info.content)

            msg = self.build_msg(message_info.subject, content, from_tag, message_info, to_address)

            server = SMTP(self.server_host, port=self.server_port)
            if self.start_tls:
                server.starttls()
            server.login(self.from_address, self.from_password)
            server.sendmail(self.from_address, to_address, msg.as_string())
            return True
        except Exception as err:
            traceback.print_exc()
            self.logger.exception('%s\t%s', err, message_info)
            return False
        finally:
            if server:
                server.quit()

    @staticmethod
    def build_msg(subject, content, from_header, message_info, to_address, charset=MessageSender.default_charset):
        # 正文
        msg = MIMEText(content, 'plain', charset)
        # 附件
        if message_info.file_paths:
            attach_msg = MIMEMultipart()
            attach_msg.attach(msg)
            for file_path in message_info.file_paths:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        # noinspection PyTypeChecker
                        att = MIMEText(f.read(), 'base64', charset)
                    att["Content-Type"] = 'application/octet-stream'
                    att["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.split(file_path)[1])
                    attach_msg.attach(att)
            msg = attach_msg

        msg["Subject"] = Header(subject, charset=charset)
        msg['From'] = Header(from_header, charset=charset)
        msg['To'] = Header(str(to_address), charset=charset)
        return msg

    @staticmethod
    def get_singleton_str(*args, **kw):
        return '-'.join(str(s) for s in (
            kw.get('server_host'), kw.get('server_port'), kw.get('start_tls'), kw.get('from_password'),
            kw.get('from_address'), kw.get('same_subject_limit_second')))

    def __hash__(self):
        return hash(self.get_singleton_str(
            server_host=self.server_host, server_port=self.server_port, start_tls=self.start_tls,
            from_password=self.from_password, from_address=self.from_address,
            same_subject_limit_second=self.same_subject_limit_second))
