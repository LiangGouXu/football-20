import logging.handlers
import datetime
import sys

# "%m/%d/%Y %H:%M:%S %p"

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logger = logging.getLogger(__name__)
# 设置日志记录级别
logger.setLevel(logging.INFO)
# 保存日志到my2.log，每天保存一个文件，最多7个
rh_logging = logging.handlers.TimedRotatingFileHandler(filename="my55.log",
                                                       when="D",
                                                       interval=1,
                                                       backupCount=7,
                                                       encoding="utf-8",
                                                       atTime=datetime.time(0, 0, 0, 0))
# 设置日志头格式
rh_logging.setFormatter(logging.Formatter(LOG_FORMAT))
# 添加 handler
logger.addHandler(rh_logging)

# 记录日志到控制台
ch = logging.StreamHandler(sys.stdout)
# 设置日志头格式
ch.setFormatter(logging.Formatter(LOG_FORMAT))
# 添加 handler
logger.addHandler(ch)


def info(msg="", **args):
    logger.info(msg=msg, **args)


def debug(msg="", **args):
    logger.debug(msg=msg, **args)


def warning(msg="", **args):
    logger.warning(msg=msg, **args)


def error(msg="", **args):
    logger.error(msg=msg, **args)


def critical(msg="", **args):
    logger.critical(msg=msg, **args)


if __name__ == '__main__':
    info("fajfsa %s" % 234)
    logger.info("This is a info log. %s" % 123)
    logger.debug("This is a debug log.")
    logger.warning("This is a warning log.")
    logger.error("This is a error log.")
    logger.critical("This is a critical log.")

