import requests
from wechatpy.client.api.base import BaseWeChatAPI

from common.log import logger


class WeChatThirdAppMessage(BaseWeChatAPI):

    base_url = "https://qyapi.weixin.qq.com/cgi-bin"

    def get_suite_token(self, suite_id, suite_secret, suite_ticket, msg=None):
        data = {
            "suite_id": suite_id,
            "suite_secret": suite_secret,
            "suite_ticket": suite_ticket
        }
        if msg is not None:
            data.update(msg)
        return requests.post(f"{self.base_url}/service/get_suite_token", json=data).json()

    def get_permanent_code(self, suite_access_token, auth_code, msg=None):
        data = {
            "auth_code": auth_code
        }
        if msg is not None:
            data.update(msg)
        return requests.post(f"{self.base_url}/service/get_permanent_code?suite_access_token={suite_access_token}", json=data).json()
