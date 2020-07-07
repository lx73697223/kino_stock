# -*- coding: utf-8 -*-

"""
发送微信公众号模版消息
"""

import json
import requests
import traceback
from datetime import datetime
from enum import Enum, unique

from utils.annotation import singleton
from message_sender import MessageSender, MessageInfo


@unique
class MessageInfoType(Enum):
    """消息内容类型"""
    STARTUP_TEMPLATE = "LmlWwRf5IDATmDiDkh2_ZdANDiMbRWI4qFCRoQcd0_U"    # 启动/注册成功模版消息


class OpenWechatMessageInfo(MessageInfo):

    def __init__(self, subject, content, to_users, message_type, url=None,
                 profile=None, from_tag=None, subject_prefix=None):
        self.message_type = message_type
        self.to_users = to_users
        self.url = url
        super().__init__(subject=subject, content=content, profile=profile, from_tag=from_tag,
                         subject_prefix=subject_prefix)


@singleton(func_name="get_singleton_str")
class OpenWechatMessageSender(MessageSender):

    default_same_subject_limit_second = -1

    def __init__(self, appid, secret, access_token_expire_seconds, send_message_url_format, access_token_url_format,
                 same_subject_limit_second=default_same_subject_limit_second, logger=None):
        self.appid = appid
        self.secret = secret
        self.access_token_expire_seconds = access_token_expire_seconds
        self.send_message_url_format = send_message_url_format
        self.access_token_url_format = access_token_url_format
        self.access_token_url = access_token_url_format % (appid, secret)
        self.access_token = None
        self.access_token_time = None
        super().__init__(logger=logger, same_subject_limit_second=same_subject_limit_second)

    def get_send_message_url(self):
        return self.send_message_url_format % self.access_token

    def get_access_token(self):
        try:
            if self.access_token and self.access_token_time:
                diff_seconds = (datetime.now() - self.access_token_time).total_seconds()
                if diff_seconds < self.access_token_expire_seconds:
                    return self.access_token
            self.access_token = requests.get(self.access_token_url, timeout=30).json().get("access_token")
            self.access_token_time = datetime.now()
            return self.access_token
        except Exception:
            traceback.print_exc()

    def send(self, message_info):
        try:
            if not message_info.to_users:
                return None

            access_token = self.get_access_token()
            if not access_token:
                self.logger.error("can not get access_token!")
                return False

            send_message_url = self.get_send_message_url()
            message_data_list = []
            if not message_info.message_type or MessageInfoType.STARTUP_TEMPLATE == message_info.message_type:
                message_data_list = self.get_strategy_startup_message_data(message_info)
            for msg in message_data_list:
                resp = requests.post(send_message_url, data=json.dumps(msg), timeout=30)
                self.logger.info(resp.json())
            return True
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('%s\t%s', e, message_info)
            return False

    @staticmethod
    def get_strategy_startup_message_data(message_info):
        msg_list = []
        for open_id in message_info.to_users:
            msg_list.append({
                "template_id": message_info.message_type.value,
                "url": message_info.url,
                "touser": open_id,
                "data": {
                    "first": {
                        "value": message_info.subject
                    },
                    "keyword1": {
                        "value": message_info.tag
                    },
                    "keyword2": {
                        "value": message_info.create_time.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    "remark": {
                        "value": "%s\n%s" % (message_info.content, open_id)
                    }
                }
            })
        return msg_list

    @staticmethod
    def get_singleton_str(*args, **kw):
        return '-'.join(str(s) for s in (
            kw.get('appid'), kw.get('secret'), kw.get('access_token_expire_seconds'),
            kw.get('send_message_url_format'), kw.get('access_token_url_format'), kw.get('same_subject_limit_second')))

    def __hash__(self):
        return hash(self.get_singleton_str(
            appid=self.appid, secret=self.secret, access_token_expire_seconds=self.access_token_expire_seconds,
            send_message_url_format=self.send_message_url_format, access_token_url_format=self.access_token_url_format,
            same_subject_limit_second=self.same_subject_limit_second))
