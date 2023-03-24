import logging
from logging import handlers
from .配置 import 配置

日志器 = logging.getLogger(name='ARIA2BOT')
日志格式 = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
流处理器 = logging.StreamHandler()
流处理器.setLevel(配置.控制台日志等级)
流处理器.setFormatter(日志格式)
日志器.addHandler(流处理器)

时旋文件处理器 = handlers.TimedRotatingFileHandler(
    filename='./log/aria2bot.log',
    when='D',
    interval=1,
    backupCount=7,
    encoding='utf-8'
)

时旋文件处理器.setLevel(配置.文件日志等级)
时旋文件处理器.setFormatter(日志格式)
日志器.addHandler(时旋文件处理器)

日志器.setLevel(logging.DEBUG)
