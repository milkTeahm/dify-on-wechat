import json
import os

from common.log import logger

# 定义JSON文件的路径
file_path = 'wework_contacts.json'  # 确保路径正确

# 查找指定用户名的用户信息
def find_user_by_username(username):
    directory = os.path.join(os.getcwd(), "asset_data", "wework")
    with open(os.path.join(directory, file_path), 'r', encoding='utf-8') as f:
        data = json.load(f)  # 加载 JSON 数据

        # 遍历 user_list 查找匹配的 username
        for user in data.get('user_list', []):
            if user.get('username').find(username) != -1:
                logger.info("匹配到用户:>>>{}".format(user["username"]))
                return user  # 返回匹配用户的信息
    return None

# 获取所有的用户信息
def find_user():
    directory = os.path.join(os.getcwd(), "asset_data", "wework")
    with open(os.path.join(directory, file_path), 'r', encoding='utf-8') as f:
        data = json.load(f)  # 加载 JSON 数据
        return data.get('user_list', [])

