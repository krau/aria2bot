import os
import re

from urllib.parse import urlparse
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
from .配置 import 配置
from .日志 import 日志器


开始键盘 = [
    ["暂停所有任务", "添加下载任务", "恢复所有任务"],
    ["活跃任务", "下载器状态", "等待中任务"],
    ["⚠️清空任务", "操作单任务", "强制下载"],
]
开始标记 = ReplyKeyboardMarkup(keyboard=开始键盘, selective=True, resize_keyboard=True)
回主菜单标记 = InlineKeyboardMarkup([[InlineKeyboardButton("回主菜单", callback_data="回主菜单")]])


async def 从消息中获取链接列表(文字消息: str) -> list:
    非磁力正则式 = r"(?:http[s]?|ftp|sftp)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"  # noqa: E501
    非磁力链接 = re.findall(非磁力正则式, 文字消息)
    磁力链接 = re.findall("magnet:\?xt=urn:btih:[0-9a-fA-F]{40,}.*", 文字消息)
    return 非磁力链接 + 磁力链接


def 仅主人装饰器(func):
    async def 包装器(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
        if 更新.effective_user.id in 配置.主人:
            await func(更新, 上下文)
        else:
            日志器.info(f"{更新.effective_user.name} 试图使用 {func.__name__} 被拒绝")

    return 包装器


async def 不是主人(用户id: int) -> None:
    if 用户id not in 配置.主人:
        日志器.info(f"{用户id} 操作被拒绝")
    return None


async def 文件单位转换(文件大小: str) -> str:
    if isinstance(文件大小, str):
        文件大小 = int(文件大小)
    if 文件大小 < 1024:
        return f"{文件大小} B"
    elif 文件大小 < 1024**2:
        return f"{文件大小 / 1024:.2f} KB"
    elif 文件大小 < 1024**3:
        return f"{文件大小 / 1024 ** 2:.2f} MB"
    elif 文件大小 < 1024**4:
        return f"{文件大小 / 1024 ** 3:.2f} GB"
    else:
        return f"{文件大小 / 1024 ** 4:.2f} TB"


async def 有机体可读下载任务详细结果(原始结果: dict) -> str:
    gid = 原始结果["gid"]
    文件 = await 获取文件名(原始结果)
    try:
        链接 = 原始结果["files"][0]["uris"][0]["uri"]
    except IndexError:
        链接 = "无"
    文件数量 = len(原始结果["files"])
    下载目录 = 原始结果["dir"]
    下载速度 = await 文件单位转换(原始结果["downloadSpeed"])
    总大小 = await 文件单位转换(原始结果["totalLength"])
    已完成 = await 文件单位转换(原始结果["completedLength"])
    try:
        下载进度 = f'{int(原始结果["completedLength"]) / int(原始结果["totalLength"]) * 100:.2f}%'
    except ZeroDivisionError:
        下载进度 = "0%"
    状态 = 原始结果["status"]
    return f"任务ID: `{gid}`\n文件: *{文件}*\n链接: {链接}\n文件数量: {文件数量}\n下载目录: *{下载目录}*\n下载速度: *{下载速度}/s*\n总大小: *{总大小}*\n已完成: *{已完成}*\n下载进度: *{下载进度}*\n状态: *{状态}*"  # noqa: E501


async def 有机体可读下载任务简略结果(原始结果: dict) -> str:
    gid = 原始结果["gid"]
    文件 = await 获取文件名(原始结果)
    下载速度 = await 文件单位转换(原始结果["downloadSpeed"])
    总大小 = await 文件单位转换(原始结果["totalLength"])
    已完成 = await 文件单位转换(原始结果["completedLength"])
    try:
        下载进度 = f'{int(原始结果["completedLength"]) / int(原始结果["totalLength"]) * 100:.2f}%'
    except ZeroDivisionError:
        下载进度 = "0%"
    return f"任务ID: `{gid}`\n文件: *{文件}*\n下载速度: *{下载速度}/s*\n总大小: *{总大小}*\n已完成: *{已完成}*\n下载进度: *{下载进度}*"  # noqa: E501


async def 有机体可读下载器状态结果(原始结果: dict) -> str:
    已启用功能列表 = 原始结果["enabledFeatures"]
    版本 = 原始结果["version"]
    有机体可读功能列表 = ""
    for 功能 in 已启用功能列表:
        有机体可读功能列表 += f"`{功能}`\n"
    return f"已启用功能: \n{有机体可读功能列表}版本: *{版本}*"


async def 有机体可读统计结果(原始结果: dict) -> str:
    活动下载数 = 原始结果["numActive"]
    下载速度 = await 文件单位转换(原始结果["downloadSpeed"])
    上传速度 = await 文件单位转换(原始结果["uploadSpeed"])
    等待下载数 = 原始结果["numWaiting"]
    已停止下载数 = 原始结果["numStopped"]
    return f"活动下载数: *{活动下载数}*\n下载速度: *{下载速度}/s*\n上传速度: *{上传速度}/s*\n等待下载数: *{等待下载数}*\n完成与停止下载数: *{已停止下载数}*"  # noqa: E501


async def 有机体可读等待任务结果(原始结果: dict) -> str:
    gid = 原始结果["gid"]
    文件 = await 获取文件名(原始结果)
    总大小 = await 文件单位转换(原始结果["totalLength"])
    try:
        链接 = 原始结果["files"][0]["uris"][0]["uri"]
    except IndexError:
        链接 = "无"
    return f"任务ID: `{gid}`\n文件: *{文件}*\n总大小: *{总大小}*\n链接: {链接}"


async def 获取文件名(任务: dict) -> str:
    if 任务.__contains__("bittorrent"):
        if 任务["bittorrent"].__contains__("info"):
            return 任务["bittorrent"]["info"]["name"]
        return 任务["files"][0]["path"]
    文件名 = 任务["files"][0]["path"].split("/")[-1]
    if 文件名 == "":
        啪 = urlparse(任务["files"][0]["uris"][0]["uri"])
        文件名 = os.path.basename(啪.path)
    return 文件名
