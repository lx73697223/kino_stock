from datetime import datetime


class MessageInfo(object):

    def __init__(self, subject, content, profile='default', from_tag=None, subject_prefix=None):
        """
        :param subject:       标题
        :param content:       内容
        :param profile:       环境
        :param from_tag:      标签
        :param subject_prefix: 标题前缀
        """
        self.content = content
        self.profile = profile
        self.from_tag = from_tag
        self.subject_prefix = subject_prefix
        self.subject = '[{}] {} {}'.format(profile, subject_prefix or '', subject)
        self.create_time = datetime.now()

    def __str__(self):
        return str(self.__dict__)
    __repr__ = __str__


class MessageSender(object):

    default_charset = "utf-8"

    def __init__(self, logger, same_subject_limit_second=-1):
        self.logger = logger
        self.same_subject_limit_second = same_subject_limit_second
        self.__send_time_map = {}

    def send(self, message_info):
        """
        :param message_info:    消息内容 type: MessageInfo
        :return:    True:发送成功，False:发送失败，None:已丢弃
        """
        raise NotImplementedError("not implemented!")

    def check_send_limit(self, send_time, message_info):
        if self.same_subject_limit_second > 0:
            key = ':'.join((message_info.subject, message_info.from_tag))
            last_sent_time = self.__send_time_map.get(key)
            if last_sent_time:
                if (send_time - last_sent_time).total_seconds() <= self.same_subject_limit_second:
                    self.logger.exception('sending too often! %s. last_sent_time: %s', key, last_sent_time)
                    return False
            self.__send_time_map[key] = send_time
        return True
