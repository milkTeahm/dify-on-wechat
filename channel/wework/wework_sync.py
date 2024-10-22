import os

os.environ['ntwork_LOG'] = "ERROR"
import ntwork

from channel.wework.wework_message import *
from common.log import logger
from channel.wework.run import wework

def get_with_retry(get_func, max_retries=5, delay=5):
    retries = 0
    result = None
    while retries < max_retries:
        result = get_func()
        if result:
            break
        logger.warning(f"获取数据失败，重试第{retries + 1}次······")
        retries += 1
        time.sleep(delay)  # 等待一段时间后重试
    return result

# 同步外部联系人（客户）
def sync_external_contacts():
    if not wework or not wework.login_status:
        logger.error("未获取到登录信息，同步失败...")
        return

    contacts = get_with_retry(wework.get_external_contacts)
    logger.info("获取联系人结束...")
    directory = os.path.join(os.getcwd(), "asset_data", "wework")
    if not contacts:
        logger.error("获取contacts失败，程序退出")
        ntwork.exit_()
        os.exit(0)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 将contacts保存到json文件中
    with open(os.path.join(directory, 'wework_contacts.json'), 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)
    return contacts

# 同步群列表
def sync_rooms():
    if not wework or not wework.login_status:
        logger.error("未获取到登录信息，同步失败...")
        return

    rooms = get_with_retry(wework.get_rooms)
    logger.info("获取聊天室结束...")
    directory = os.path.join(os.getcwd(), "asset_data", "wework")
    if not rooms:
        logger.error("获取rooms失败，程序退出")
        ntwork.exit_()
        os.exit(0)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 将contacts保存到json文件中
    with open(os.path.join(directory, 'wework_rooms.json'), 'w', encoding='utf-8') as f:
        json.dump(rooms, f, ensure_ascii=False, indent=4)
    return rooms

# 同步群成员
def sync_room_members(rooms):
    if not wework or not wework.login_status:
        logger.error("未获取到登录信息，同步失败...")
        return

    directory = os.path.join(os.getcwd(), "asset_data", "wework")
    # 创建一个空字典来保存结果
    result = {}
    # 遍历列表中的每个字典
    for room in rooms['room_list']:
        # 获取聊天室ID
        room_wxid = room['conversation_id']
        # 获取聊天室成员
        room_members = wework.get_room_members(room_wxid)
        # 将聊天室成员保存到结果字典中
        result[room_wxid] = room_members
    # 将结果保存到json文件中
    with open(os.path.join(directory, 'wework_room_members.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return result