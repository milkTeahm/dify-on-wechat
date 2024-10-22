import json
import os

from common.log import logger

# 定义JSON文件的路径
file_path = 'wechatcomthird_client.json'
suite_ticket_path = 'wechatcomthird_suiteticket.json'
auth_path = 'wechatcomthird_auth.json'

def exists_file(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_client_info(clientInfo):
    directory = os.path.join(os.getcwd(), "tmp")
    exists_file(directory)
    # 读取已有 JSON 文件中的数据
    existing_data = get_client_info()
    new_data = []
    # 如果已经有了，先排除
    for client_info in existing_data:
        if client_info["auth_corp_info"]["corpid"] != clientInfo["auth_corp_info"]["corpid"]:
            new_data.append(client_info)
    new_data.append(clientInfo)
    # 将client保存到json文件中
    with open(os.path.join(directory, file_path), 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

# 获取所有的客户端信息
def get_client_info():
    directory = os.path.join(os.getcwd(), "tmp")
    try:
        with open(os.path.join(directory, file_path), 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []
    return existing_data

def save_suite_ticket(suiteticket):
    directory = os.path.join(os.getcwd(), "tmp")
    exists_file(directory)
    # 将client保存到json文件中
    with open(os.path.join(directory, suite_ticket_path), 'w', encoding='utf-8') as f:
        json.dump(suiteticket, f, ensure_ascii=False, indent=4)

# 获取最新的suiteticket信息
def get_suite_ticket():
    directory = os.path.join(os.getcwd(), "tmp")
    try:
        with open(os.path.join(directory, suite_ticket_path), 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = None
    return existing_data

def save_auth(auth):
    directory = os.path.join(os.getcwd(), "tmp")
    exists_file(directory)
    # 读取已有 JSON 文件中的数据
    existing_data = get_auth()
    existing_data.append(auth)
    # 将auth保存到json文件中
    with open(os.path.join(directory, auth_path), 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

# 获取当前所有的auth信息
def get_auth():
    directory = os.path.join(os.getcwd(), "tmp")
    try:
        with open(os.path.join(directory, auth_path), 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []
    return existing_data

# 根据auth_code删除对应的数据
def delete_auth(auth_codes_to_delete):
    directory = os.path.join(os.getcwd(), "tmp")
    # 读取已有 JSON 文件中的数据
    existing_data = get_auth()
    # 筛选出不在要删除列表中的数据
    new_data = [item for item in existing_data if item['AuthCode'] not in auth_codes_to_delete]
    # 将新的数据保存到json文件中
    with open(os.path.join(directory, auth_path), 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
