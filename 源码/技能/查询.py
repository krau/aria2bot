from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram.error import BadRequest

from ..小工具 import 仅主人装饰器, 有机体可读下载任务结果, 有机体可读下载器状态结果, 有机体可读统计结果, 有机体可读等待任务结果
from ..小工具 import 开始标记
from ..日志 import 日志器
from ..下载器 import 获取下载器
from ..配置 import 配置

查询活跃刷新标记 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('刷新', callback_data='刷新活跃任务'), InlineKeyboardButton(
        '回主菜单', callback_data='回主菜单')],
])


@仅主人装饰器
async def 查询活跃任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 请求查询活跃任务')
    try:
        async with 获取下载器() as 下载器:
            结果: list = await 下载器.tellActive(keys=['gid', 'dir', 'downloadSpeed', 'totalLength', 'completedLength', 'files'])
        if not 结果:
            await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='当前没有下载任务')
            return
        好结果 = ''
        for 任务 in 结果:
            好结果 = 好结果 + await 有机体可读下载任务结果(任务) + '\n\n'
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'当前活跃任务:\n\n{好结果}',
                                   parse_mode='Markdown', reply_markup=查询活跃刷新标记)
    except Exception as e:
        日志器.error(f'查询活跃任务出错,错误信息:\n {e.__class__.__name__}: {e}')
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'查询活跃任务出错,错误信息:\n {e.__class__.__name__}: {e}')


@仅主人装饰器
async def 刷新活跃任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 请求刷新活跃任务')
    try:
        async with 获取下载器() as 下载器:
            结果: list = await 下载器.tellActive(keys=['gid', 'dir', 'downloadSpeed', 'totalLength', 'completedLength', 'files'])
        if not 结果:
            await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='所有任务已完成')
            return
        好结果 = ''
        for 任务 in 结果:
            好结果 = 好结果 + await 有机体可读下载任务结果(任务) + '\n\n'
        await 上下文.bot.edit_message_text(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id,
                                        text=f'当前活跃任务:\n\n{好结果} 共有{len(结果)}个活跃任务', parse_mode='Markdown', reply_markup=查询活跃刷新标记)
    except BadRequest:
        """状态无变化时的处理"""
        await 上下文.bot.edit_message_text(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id,
                                        text=f'当前活跃任务:\n\n{好结果} _当前状态无变化_', parse_mode='Markdown', reply_markup=查询活跃刷新标记)
    except Exception as e:
        日志器.error(f'刷新活跃任务出错,错误信息:\n {e.__class__.__name__}: {e}')
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'刷新活跃任务出错,错误信息:\n {e.__class__.__name__}: {e}')


查询等待刷新标记 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('刷新', callback_data='刷新等待中任务'), InlineKeyboardButton(
        '回主菜单', callback_data='回主菜单')],
])


@仅主人装饰器
async def 查询等待中任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 请求查询等待中任务')
    try:
        async with 获取下载器() as 下载器:
            结果: list = await 下载器.tellWaiting(offset=0, num=114514, keys=['gid', 'dir', 'totalLength', 'files'])
        if not 结果:
            await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='当前没有等待中任务')
            return
        好结果 = ''
        for 任务 in 结果[:10]:
            好结果 = 好结果 + await 有机体可读等待任务结果(任务) + '\n\n'
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'当前等待中任务共{len(结果)}个,最多显示前10条:\n\n{好结果}', parse_mode='Markdown', reply_markup=查询等待刷新标记)
    except Exception as e:
        日志器.error(f'查询等待中任务出错,错误信息:\n {e.__class__.__name__}: {e}')
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'查询等待中任务出错,错误信息:\n {e.__class__.__name__}: {e}')


@仅主人装饰器
async def 刷新等待中任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 请求刷新等待中任务')
    try:
        async with 获取下载器() as 下载器:
            结果: list = await 下载器.tellWaiting(offset=0, num=114514, keys=['gid', 'dir', 'totalLength', 'files'])
        if not 结果:
            await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='当前没有等待中任务')
            return
        好结果 = ''
        for 任务 in 结果[:10]:
            好结果 = 好结果 + await 有机体可读等待任务结果(任务) + '\n\n'
        await 上下文.bot.edit_message_text(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id,
                                        text=f'最多显示前10条等待中任务:\n\n{好结果} 当前等待中任务共{len(结果)}个', parse_mode='Markdown', reply_markup=查询等待刷新标记)
    except BadRequest:
        """状态无变化时的处理"""
        await 上下文.bot.edit_message_text(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id,
                                        text=f'最多显示前10条等待中任务:\n\n{好结果} _当前状态无变化_', parse_mode='Markdown', reply_markup=查询等待刷新标记)
    except Exception as e:
        日志器.error(f'刷新等待中任务出错,错误信息:\n {e.__class__.__name__}: {e}')
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'刷新等待中任务出错,错误信息:\n {e.__class__.__name__}: {e}')


@仅主人装饰器
async def 回主菜单(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    await 上下文.bot.delete_message(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id)
    await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='请选择操作:', reply_markup=开始标记)


查询下载器刷新标记 = InlineKeyboardMarkup([[InlineKeyboardButton(
    '刷新', callback_data='刷新下载器状态'), InlineKeyboardButton('回主菜单', callback_data='回主菜单')]])


@仅主人装饰器
async def 查询下载器状态(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 请求查询下载器状态')
    try:
        async with 获取下载器() as 下载器:
            本体结果: dict = await 下载器.getVersion()
            统计结果: dict = await 下载器.getGlobalStat()
        好结果 = await 有机体可读下载器状态结果(本体结果) + '\n\n' + await 有机体可读统计结果(统计结果) + '\n\n' + f'RPC地址: {配置.下载器地址}'
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'{好结果}', parse_mode='Markdown', reply_markup=查询下载器刷新标记)
    except Exception as e:
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'查询下载器状态出错,错误信息:\n {e.__class__.__name__}: {e}')


@仅主人装饰器
async def 刷新下载器状态(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    日志器.info(f'{更新.effective_user.name} 请求刷新下载器状态')
    try:
        async with 获取下载器() as 下载器:
            本体结果: dict = await 下载器.getVersion()
            统计结果: dict = await 下载器.getGlobalStat()
        好结果 = await 有机体可读下载器状态结果(本体结果) + '\n\n' + await 有机体可读统计结果(统计结果) + '\n\n' + f'RPC地址: {配置.下载器地址}'
        await 上下文.bot.edit_message_text(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id,
                                        text=f'{好结果}', parse_mode='Markdown', reply_markup=查询下载器刷新标记)
    except BadRequest:
        """状态无变化时的处理"""
        await 上下文.bot.edit_message_text(chat_id=更新.effective_chat.id, message_id=更新.callback_query.message.message_id,
                                        text=f'{好结果}\n_当前状态无变化_', parse_mode='Markdown', reply_markup=查询下载器刷新标记)
    except Exception as e:
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'刷新下载器状态出错,错误信息:\n {e.__class__.__name__}: {e}')

查询活跃任务处理器 = MessageHandler(filters.Regex('查询活跃任务'), 查询活跃任务)

刷新活跃任务处理器 = CallbackQueryHandler(刷新活跃任务, pattern='刷新活跃任务')

查询下载器状态处理器 = MessageHandler(filters.Regex('查询下载器状态'), 查询下载器状态)

查询等待中任务处理器 = MessageHandler(filters.Regex('查询等待中任务'), 查询等待中任务)

刷新等待中任务处理器 = CallbackQueryHandler(刷新等待中任务, pattern='刷新等待中任务')

刷新下载器状态处理器 = CallbackQueryHandler(刷新下载器状态, pattern='刷新下载器状态')

回主菜单处理器 = CallbackQueryHandler(回主菜单, pattern='回主菜单')
