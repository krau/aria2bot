from aioaria2 import Aria2HttpClient
from contextlib import asynccontextmanager
from .配置 import 配置


@asynccontextmanager
async def 获取下载器():
    下载器 = Aria2HttpClient(url=配置.下载器组[0].下载器地址, token=配置.下载器组[0].下载器配置)
    try:
        yield 下载器
    finally:
        await 下载器.close()
