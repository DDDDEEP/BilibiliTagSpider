#!/usr/bin/env python
"""处理某个分区下，一段日期内的视频，所包含的标签。"""

import io
import sys

from proxypool.scheduler import Scheduler
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    s = Scheduler()
    s.run()


if __name__ == '__main__':
    main()
