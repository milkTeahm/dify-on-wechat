# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import xmltodict

from wechatpy.enterprise.events import EVENT_TYPES
from wechatpy.enterprise.messages import MESSAGE_TYPES
from wechatpy.messages import UnknownMessage
from wechatpy.utils import to_text


def wechat_thirdapp_parse_message(xml):
    if not xml:
        return
    message = xmltodict.parse(to_text(xml))['xml']
    return message
