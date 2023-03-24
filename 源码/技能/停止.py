from ..小工具 import 仅主人装饰器, 有机体可读统计结果, 回主菜单标记
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from ..下载器 import 获取下载器
from ..日志 import 日志器


@仅主人装饰器
async def 取消暂停所有任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 取消暂停所有任务')
    async with 获取下载器() as 下载器:
        await 下载器.unpauseAll()
    await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='已取消暂停所有任务')


@仅主人装饰器
async def 暂停所有任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 暂停所有任务')
    async with 获取下载器() as 下载器:
        await 下载器.pauseAll()
    await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='已暂停所有任务')


请求清空任务标记 = InlineKeyboardMarkup(
    [[InlineKeyboardButton('确认', callback_data='确认清空任务'),
      InlineKeyboardButton('取消', callback_data='回主菜单')]])


@仅主人装饰器
async def 请求清空任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.warning(f'{更新.effective_user.name} 请求清空任务')
    async with 获取下载器() as 下载器:
        统计结果 = await 下载器.getGlobalStat()
    好结果 = await 有机体可读统计结果(统计结果)
    提醒 = f"""
    *此操作将清空所有任务与记录*,包括正在下载,等待队列,已暂停和已完成的任务.
但默认情况下,已下载的文件不会被删除.
如果想删除已下载的文件,请通过在aria2的配置文件中设置 `on-download-complete` 选项来实现.
当前状态:
{好结果}

*请确认是否要清空任务*
    """
    await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=提醒,
                               reply_markup=请求清空任务标记, parse_mode='Markdown')


@仅主人装饰器
async def 确认清空任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.warning(f'{更新.effective_user.name} 确认清空任务')
    async with 获取下载器() as 下载器:
        活跃的任务 = await 下载器.tellActive()
        if 活跃的任务:
            for 任务 in 活跃的任务:
                await 下载器.forceRemove(任务['gid'])
        等待的任务 = await 下载器.tellWaiting(0, 114514)
        if 等待的任务:
            for 任务 in 等待的任务:
                await 下载器.forceRemove(任务['gid'])
        await 下载器.forcePauseAll()
        await 下载器.purgeDownloadResult()
    await 上下文.bot.edit_message_text(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id,
                                    text='已清空任务')

取消暂停所有任务处理器 = MessageHandler(
    filters=filters.Regex('取消暂停所有任务'), callback=取消暂停所有任务)
暂停所有任务处理器 = MessageHandler(filters=filters.Regex('暂停所有任务'), callback=暂停所有任务)
确认清空任务处理器 = CallbackQueryHandler(pattern='确认清空任务', callback=确认清空任务)
请求清空任务处理器 = MessageHandler(filters=filters.Regex('清空任务'), callback=请求清空任务)
