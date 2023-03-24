import os

from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler

from 源码.小工具 import 仅主人装饰器, 开始标记
from 源码.日志 import 日志器
from 源码.配置 import 配置
from 源码.技能.下载 import 添加下载任务处理器
from 源码.技能.查询 import 查询活跃任务处理器, 刷新活跃任务处理器, 回主菜单处理器, 查询下载器状态处理器
from 源码.技能.查询 import 查询等待中任务处理器, 刷新等待中任务处理器, 刷新下载器状态处理器
from 源码.技能.停止 import 取消暂停所有任务处理器, 暂停所有任务处理器, 确认清空任务处理器, 请求清空任务处理器

if not os.path.exists('log'):
    os.mkdir('log')

日志器.info('Aria2Bot启动中...')
if 配置.代理地址:
    日志器.debug(f'设置代理为: {配置.代理地址}')
    os.environ['HTTP_PROXY'] = 配置.代理地址
    os.environ['HTTPS_PROXY'] = 配置.代理地址


@仅主人装饰器
async def 开始(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 执行了/start')
    await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='欢迎使用Aria2Bot', reply_markup=开始标记)


def 跑():
    应用 = ApplicationBuilder().token(配置.机器人密钥).build()
    应用._concurrent_updates = False

    开始处理器 = CommandHandler('start', 开始)

    处理器组 = [
        开始处理器,
        添加下载任务处理器,
        查询活跃任务处理器,
        刷新活跃任务处理器,
        回主菜单处理器,
        查询下载器状态处理器,
        查询等待中任务处理器,
        刷新等待中任务处理器,
        刷新下载器状态处理器,
        取消暂停所有任务处理器,
        暂停所有任务处理器,
        确认清空任务处理器,
        请求清空任务处理器,
    ]
    应用.add_handlers(处理器组)
    日志器.info('Aria2Bot已启动')
    应用.run_polling()


if __name__ == '__main__':
    跑()
