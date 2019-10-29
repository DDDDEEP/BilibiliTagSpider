import unittest
import logging
from proxypool.log import logger

# 测试用例存放路径
case_path = './test'


def get_allcase():
    # 获取所有测试用例
    discover = unittest.defaultTestLoader.discover(
        case_path, pattern="test*.py")
    suite = unittest.TestSuite()
    suite.addTest(discover)
    return suite


if __name__ == '__main__':
    # 运行测试用例
    runner = unittest.TextTestRunner()
    runner.run(get_allcase())
