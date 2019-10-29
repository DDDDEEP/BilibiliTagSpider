import logging
from proxypool.setting import LOG_LEVEL, LOG_STDOUT

# 设置日志对象
logger = logging.getLogger('ProxyPool')
logger.setLevel(level=LOG_LEVEL)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
