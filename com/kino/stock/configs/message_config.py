"""
消息配置
邮箱参数
微信公众号参数
"""


class MessageConfig(object):
    success_subject_prefix = '|success|'
    error_subject_prefix = '!error!'
    error_forward_subject_prefix = '!error-forward!'

    # email
    message_starttls = False
    message_server_host = None
    message_server_port = None
    message_from_address = None
    message_from_password = None
    message_to_address = []
    message_webclient_url = None

    # open_wechat
    open_wechat_appid = None
    open_wechat_secret = None
    open_wechat_to_user_ids = []
    # access_token
    access_token_expire_seconds = 7000
    open_wechat_get_access_token_url_format = \
        "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
    # send_message
    open_wechat_send_message_url_format = \
        "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"
