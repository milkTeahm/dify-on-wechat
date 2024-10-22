import threading
import time

from wechatpy.enterprise import WeChatClient

from channel.wechatcomthird.wechatthirdapp_message import WeChatThirdAppMessage


class WechatComThirdAppClient(WeChatClient):
    def __init__(self, corp_id, secret, access_token=None, session=None, timeout=None, auto_retry=True):
        super(WechatComThirdAppClient, self).__init__(corp_id, secret, access_token, session, timeout, auto_retry)
        self.fetch_access_token_lock = threading.Lock()
        self.message = WeChatThirdAppMessage(self)

    def fetch_access_token(self):  # 重载父类方法，加锁避免多线程重复获取access_token
        with self.fetch_access_token_lock:
            access_token = self.session.get(self.access_token_key)
            if access_token:
                if not self.expires_at:
                    return access_token
                timestamp = time.time()
                if self.expires_at - timestamp > 60:
                    return access_token
            return super().fetch_access_token()
