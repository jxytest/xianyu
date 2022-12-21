import threading

from apscheduler.schedulers.background import BackgroundScheduler

from .xy_task import start_task


class TaskManage:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.start()
        self.job_id = None

    def add_interval_task(self, func, seconds: int, args=None):
        self.job_id = self.scheduler.add_job(func, 'interval', seconds=seconds, args=args, replace_existing=True)

    def update_interval_task(self, func, seconds: int, args=None):
        # 重新添加
        if self.job_id:
            self.add_interval_task(func, seconds, args)
        else:
            raise Exception("任务不存在")

    def del_interval_task(self):
        self.scheduler.remove_job(self.job_id)
        self.job_id = None

    def task_list(self):
        return self.scheduler.get_jobs()

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def pause(self):
        self.scheduler.pause()

    def resume(self):
        self.scheduler.resume()


class XianYuTask(TaskManage):
    def __init__(self):
        super().__init__()
        self.look = threading.Lock()
        self.keywords = []

    def add_task(self, keywords, seconds: int):
        with self.look:
            self.keywords.extend(keywords)
            self.add_interval_task(start_task, seconds, args=[self.keywords])

    def update_task(self, keywords, seconds: int):
        with self.look:
            self.keywords = keywords
            self.update_interval_task(start_task, seconds, args=[self.keywords])

    def del_task(self, keywords, seconds: int):
        with self.look:
            for keyword in keywords:
                if keyword in self.keywords:
                    self.keywords.remove(keyword)
            self.update_interval_task(start_task, seconds, args=[self.keywords])

    def clear_task(self):
        with self.look:
            self.keywords.clear()
            self.update_interval_task(start_task, 1000, args=[self.keywords])

    def task_count(self):
        return len(self.keywords)

    def task_list(self):
        return self.keywords

