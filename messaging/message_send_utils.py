# -*- coding: utf-8 -*-

import traceback

from configs.app_config import AppConfig
from configs.message_config import MessageConfig
from core_utils.annotation import async_exec
from core_utils.logging_utils import LoggingUtil, log
from messaging.email_message_sender import EmailMessageSender, EmailMessageInfo
from messaging.open_wechat_message_sender import OpenWechatMessageSender, OpenWechatMessageInfo


logger = LoggingUtil.get_default_logger()


@async_exec
def send_email_async(subject, content, file_paths=None, profile=None, from_tag=None, subject_prefix=None):
    return send_email(subject=subject, content=content, file_paths=file_paths, subject_prefix=subject_prefix,
                      profile=profile or AppConfig.profile, from_tag=from_tag or AppConfig.get_app_tag())


@async_exec
def send_open_wechat_msg_async(subject, content, to_users=None, from_tag=None, subject_prefix=None):
    return send_open_wechat_msg(subject, content=content, to_users=to_users, subject_prefix=subject_prefix,
                                from_tag=from_tag or AppConfig.get_app_tag())


@log(log_result=True)
def send_email(subject, content, file_paths=None, profile=None, from_tag=None, subject_prefix=None):
    try:
        sender = EmailMessageSender(
            server_host=MessageConfig.message_server_host, server_port=MessageConfig.message_server_port,
            start_tls=MessageConfig.message_starttls, from_password=MessageConfig.message_from_password,
            from_address=MessageConfig.message_from_address, logger=logger)
        message_info = EmailMessageInfo(
            subject=subject, content=content, file_paths=file_paths, to_address=MessageConfig.message_to_address,
            profile=profile or AppConfig.profile, from_tag=from_tag or AppConfig.get_app_tag(),
            subject_prefix=subject_prefix)
        result = sender.send(message_info)
        if result is False:
            raise Exception("send_email failed! result={}".format(result))
        return result
    except Exception as e:
        traceback.print_exc()
        logger.exception("send_email failed: %s! subject_prefix=%s", e, subject_prefix)
        # 换个方式发送
        if MessageConfig.error_forward_subject_prefix != subject_prefix:
            send_open_wechat_msg(subject, content="{};e:{}".format(content, e), message_type=None, from_tag=from_tag,
                                 subject_prefix=MessageConfig.error_forward_subject_prefix)


@log(log_result=True)
def send_open_wechat_msg(subject, content, to_users=None, message_type=None, from_tag=None, subject_prefix=None):
    try:
        sender = OpenWechatMessageSender(
            appid=MessageConfig.open_wechat_appid, secret=MessageConfig.open_wechat_secret,
            access_token_expire_seconds=MessageConfig.access_token_expire_seconds,
            send_message_url_format=MessageConfig.open_wechat_send_message_url_format,
            access_token_url_format=MessageConfig.open_wechat_get_access_token_url_format, logger=logger)
        message_info = OpenWechatMessageInfo(
            subject=subject, content=content, message_type=message_type, url=MessageConfig.message_webclient_url,
            to_users=to_users or MessageConfig.open_wechat_to_user_ids, from_tag=from_tag or AppConfig.get_app_tag(),
            subject_prefix=subject_prefix)
        result = sender.send(message_info)
        if result is False:
            raise Exception("send_open_wechat_msg failed! result={}".format(result))
        return result
    except Exception as e:
        traceback.print_exc()
        logger.exception("send_open_wechat_msg failed: %s! subject_prefix=%s", e, subject_prefix)
        # 换个方式发送
        if MessageConfig.error_forward_subject_prefix != subject_prefix:
            send_email(subject, content="{}\nerror: {}".format(content, e), from_tag=from_tag,
                       subject_prefix=MessageConfig.error_forward_subject_prefix)
