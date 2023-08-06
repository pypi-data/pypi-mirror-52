import logging

from rocketchat_API.rocketchat import RocketChat


class RocketLogHandler(logging.Handler):
    rc = None
    channel = None
    alias = None

    def __init__(self, rc_user, rc_token, rc_server, rc_channel, rc_alias):
        super().__init__()
        self.rc = RocketChat(user_id=rc_user, auth_token=rc_token, server_url=rc_server)
        self.channel = rc_channel
        self.alias = rc_alias

    def emit(self, record):
        self.rc.chat_post_message(self.format(record), channel=self.channel, alias=self.alias)
