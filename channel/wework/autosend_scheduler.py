from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler

from bridge.context import Context, ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from channel.wework.getContactUser import find_user_by_username, find_user
from common.log import logger

class AutoSendScheduler:
    def __init__(self, weworkChannel):
        # 初始化调度器
        self.scheduler = BackgroundScheduler()
        self.channel = weworkChannel

    def send_msg(self, content: str):
        reply = Reply(ReplyType.TEXT, content)
        context = Context(ContextType.TEXT, content)
        receiver = find_user_by_username("一杯杨枝甘露")
        if receiver is None:
            logger.info("[WX] 没有获取到对应的用户")
            return
        context["receiver"] = receiver["conversation_id"]
        msg = ChatMessage(None)
        msg.actual_user_id = self.channel.user_id
        context["msg"] = msg
        self.channel.send_reply(context, reply)

    def send_all(self, content: str):
        # 获取所有的用户
        receivers = find_user()
        if receivers is []:
            logger.info("[WX] 没有获取到用户")
            return
        # 遍历用户发送消息
        for receiver in receivers:
            # 组装发送数据
            reply = Reply(ReplyType.TEXT, content)
            context = Context(ContextType.TEXT, content)
            context["receiver"] = receiver["conversation_id"]
            msg = ChatMessage(None)
            msg.actual_user_id = self.channel.user_id
            context["msg"] = msg
            self.channel.send_reply(context, reply)


    # 任务函数
    def job_morning(self):
        logger.info("[WX] 任务开始执行...")
        self.send_msg("这是定时发送的消息，不用管...")
        logger.info("[WX] 任务执行完成...")

    def job_night(self):
        logger.info("[WX] 任务开始执行...")
        self.send_msg("晚上好")
        logger.info("[WX] 任务执行完成...")

    def schedule_jobs(self):
        logger.info("[WX] 创建定时任务")
        # 添加每天早上9点执行任务
        # self.scheduler.add_job(self.job_morning, 'cron', hour=17, minute=25)
        run_time = datetime.now() + timedelta(seconds=10)
        self.scheduler.add_job(self.job_morning, 'date', run_date=run_time)
        # 添加每天晚上9点执行任务
        self.scheduler.add_job(self.job_night, 'cron', hour=21, minute=0)

    def start(self):
        # self.schedule_jobs()
        # # 检查调度器是否已经启动
        # if self.scheduler.running:
        #     logger.info("Scheduler is already running. Stopping it now.")
        #     self.scheduler.shutdown()  # 如果已启动，则停止调度器
        # # 开始调度器
        # self.scheduler.start()
        logger.info("启动定时任务...")

    def stop(self):
        # 停止调度器
        self.scheduler.shutdown()