from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler
from aioaria2 import Aria2rpcException

from ..小工具 import 不是主人, 仅主人装饰器, 从消息中获取链接列表, 回主菜单标记
from ..日志 import 日志器
from ..下载器 import 获取下载器


REPLY = range(1)
添加下载任务成功标记 = InlineKeyboardMarkup([[InlineKeyboardButton(
    '查看活跃任务详情', callback_data='刷新活跃任务'), InlineKeyboardButton('回主菜单', callback_data='回主菜单')]])


async def 添加下载任务回复中(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE) -> int:
    日志器.info(f'{更新.effective_user.name} 请求添加下载任务')
    强制回复标记 = ForceReply(
        input_field_placeholder='请发送链接,支持http(s)|ftp|sftp|magnet,支持一次发送多个链接')
    await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='请发送下载链接', reply_markup=强制回复标记)
    return REPLY


async def 添加下载任务已回复(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE) -> int:
    if await 不是主人(更新.effective_user.id):
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=await 不是主人(更新.effective_user.id))
        return ConversationHandler.END
    日志器.info(f'{更新.effective_user.name} 已回复添加下载任务')
    下载链接列表 = await 从消息中获取链接列表(更新.effective_message.text)
    if not 下载链接列表:
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='未检测到下载链接', reply_markup=回主菜单标记)
        return ConversationHandler.END
    try:
        async with 获取下载器() as 下载器:
            for 单链接 in 下载链接列表:
                单链接列表 = [单链接]
                await 下载器.addUri(uris=单链接列表)
        有机体可读下载链接列表 = '\n'.join(下载链接列表)
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'已添加到下载队列:\n\n{有机体可读下载链接列表}', parse_mode='Markdown', reply_markup=添加下载任务成功标记)
    except Aria2rpcException as e:
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'添加下载任务失败,Aria2rpc异常:\n _{e}_', parse_mode='Markdown', reply_markup=回主菜单标记)
    except Exception as e:
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'添加下载任务失败,未知异常:\n _{e}_', parse_mode='Markdown', reply_markup=回主菜单标记)
    finally:
        return ConversationHandler.END


添加下载任务处理器 = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('添加下载任务'), 添加下载任务回复中)],
    states={REPLY: [
        MessageHandler(~filters.COMMAND, 添加下载任务已回复)
    ]
    },
    fallbacks=[MessageHandler(~filters.COMMAND, 添加下载任务已回复)]
)
