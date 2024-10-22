
from apscheduler.schedulers.background import BackgroundScheduler
from channel.wework.wework_sync import sync_external_contacts, sync_rooms, sync_room_members
from common.log import logger

class AutoSyncWeworkScheduler:
    def __init__(self, weworkChannel):
        # 初始化调度器
        self.scheduler = BackgroundScheduler()
        self.channel = weworkChannel

    # 任务函数
    def job_sync_external_contacts(self):
        logger.info("[WX] 定时任务：同步联系人...")
        sync_external_contacts()
        logger.info("[WX] 定时任务：同步联系人结束...")

    def job_sync_rooms(self):
        logger.info("[WX] 定时任务：同步聊天室...")
        rooms = sync_rooms()
        sync_room_members(rooms)
        logger.info("[WX] 定时任务：同步聊天室结束...")

    def schedule_jobs(self):
        logger.info("[WX] 创建定时同步任务")
        # 添加定时任务，每小时执行一次
        self.scheduler.add_job(self.job_sync_external_contacts, 'interval', hours=1)
        self.scheduler.add_job(self.job_sync_rooms, 'interval', hours=1)

    def start(self):
        self.schedule_jobs()
        # 检查调度器是否已经启动
        if self.scheduler.running:
            logger.info("AutoSyncWeworkScheduler is already running. Stopping it now.")
            self.scheduler.shutdown()  # 如果已启动，则停止调度器
        # 开始调度器
        self.scheduler.start()
        logger.info("启动数据同步定时任务...")

    def stop(self):
        # 停止调度器
        self.scheduler.shutdown()