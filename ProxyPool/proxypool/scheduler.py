"""代理池功能调度器"""
import time
import logging
from multiprocessing import Process

from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
import proxypool.setting as setting

logger = logging.getLogger('ProxyPool')


class Scheduler():
    def schedule_tester(self, cycle=setting.TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            logger.info('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=setting.GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            logger.info('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        app.run(setting.API_HOST, setting.API_PORT)

    def run(self):
        logger.info('代理池开始运行')

        if setting.TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if setting.GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if setting.API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
