# -*- coding=utf-8 -*-
import web
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import to_text

from channel.chat_channel import ChatChannel
from channel.wechatcomthird.auth_util import save_suite_ticket, save_client_info, \
    get_suite_ticket
from channel.wechatcomthird.wechatcomthirdapp_client import WechatComThirdAppClient
from channel.wechatcomthird.wechatthirdapp_message import WeChatThirdAppMessage
from channel.wechatcomthird.wechatthirdapp_parse_message import wechat_thirdapp_parse_message
from common.log import logger
from common.singleton import singleton
from config import conf

MAX_UTF8_LEN = 2048


@singleton
class WechatComThirdAppChannel(ChatChannel):
    NOT_SUPPORT_REPLYTYPE = []
    message:WeChatThirdAppMessage  = None
    def __init__(self):
        super().__init__()
        self.corp_id = conf().get("wechatcomappthird_corp_id")
        self.agent_id = conf().get("wechatcomappthird_agent_id")
        self.secret = conf().get("wechatcomappthird_secret")
        self.token = conf().get("wechatcomappthird_token")
        self.aes_key = conf().get("wechatcomappthird_aes_key")
        print(self.corp_id, self.token, self.aes_key)
        logger.info(
            "[wechatcomthird] init: corp_id: {}, token: {}, aes_key: {}".format(self.corp_id, self.token, self.aes_key)
        )
        self.client = WechatComThirdAppClient(self.corp_id, self.secret)
        self.crypto = WeChatCrypto(self.token, self.aes_key, self.agent_id)
        logger.info("[wechatcomthird] 初始化完成")

    def startup(self):
        # start message listener
        urls = ("/wxcomapp/?", "channel.wechatcomthird.wechatcomthirdapp_channel.Query")
        app = web.application(urls, globals(), autoreload=False)
        port = conf().get("wechatcomappthird_port", 9898)
        web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", port))


class Query:
    def GET(self):
        channel = WechatComThirdAppChannel()
        params = web.input()
        logger.info("[wechatcomthird] receive params: {}".format(params))
        try:
            signature = params.msg_signature
            timestamp = params.timestamp
            nonce = params.nonce
            echostr = params.echostr
            echostr = channel.crypto.check_signature(signature, timestamp, nonce, echostr)
        except InvalidSignatureException:
            raise web.Forbidden()
        return echostr

    def POST(self):
        channel = WechatComThirdAppChannel()
        params = web.input()
        logger.info("[wechatcomthird] receive params: {}".format(params))
        import xmltodict
        logger.info("[wechatcomthird] receive data: {}".format(xmltodict.parse(to_text(web.data()))['xml']))
        try:
            signature = params.msg_signature
            timestamp = params.timestamp
            nonce = params.nonce
            message = channel.crypto.decrypt_message(web.data(), signature, timestamp, nonce)
        except (InvalidSignatureException, InvalidCorpIdException)  as e:
            logger.error(f"[wechatcomthird] Error: {e}")
            raise web.Forbidden()
        logger.info("[wechatcomthird] receive message: {}".format(message))
        msg = wechat_thirdapp_parse_message(message)
        logger.info("[wechatcomthird] receive message-json: {}".format(msg))
        info_type = msg['InfoType'].lower()
        if info_type == 'suite_ticket':
            save_suite_ticket(msg)
        elif info_type == 'create_auth':
            self.get_third_secret(channel, msg)
        logger.info("[wechatcomthird] receive message: {}, msg= {}".format(message, msg))

        return "success"

    def get_third_secret(self, channel, auth):
        suite_ticket = get_suite_ticket()
        if suite_ticket is None:
            logger.info("[wechatcomthird] 还未接收到suite_ticket消息")
            return
        # 获取第三方应用凭证
        suite_token = channel.client.message.get_suite_token(channel.agent_id, channel.secret, suite_ticket["SuiteTicket"])
        logger.info("[wechatcomthird] get suite_token: {}".format(suite_token))
        if suite_token["suite_access_token"] is None:
            logger.info("[wechatcomthird] 获取suite_access_token错误")
            return
        # 获取企业永久授权码
        permanent_code = channel.client.message.get_permanent_code(suite_token["suite_access_token"], auth["AuthCode"])
        logger.info("[wechatcomthird] get permanent_code: {}".format(permanent_code))
        if permanent_code["permanent_code"]:
            save_client_info(permanent_code)



