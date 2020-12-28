import logging, os
from Common.common_methods import func
from Config.file_path import log_dir


class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.log_path, encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # 在控制台输出
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义hanler的格式
        formatter = logging.Formatter(self.fmt)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给log添加handles
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def fmt(self):
        return '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'

    @property
    def log_path(self):
        func.mkdir_dir(log_dir)
        return os.path.join(log_dir, 'test{}.log'.format(func.get_time(fmt='%Y%m%d')))


log = Logger().logger
if __name__ == '__main__':
    log.info("你好")

