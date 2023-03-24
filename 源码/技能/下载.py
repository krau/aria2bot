from telegram import Update, ForceReply
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler
from aioaria2 import Aria2rpcException

from ..小工具 import 不是主人, 仅主人装饰器
from ..日志 import 日志器
from ..下载器 import 获取下载器


REPLY = range(1)


async def 添加下载任务回复中(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE) -> int:
    日志器.info(f'{更新.effective_user.name} 请求添加下载任务')
    强制回复标记 = ForceReply(
        input_field_placeholder='请发送单个链接,支持http(s)|ftp|sftp|magnet')
    await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text='请发送下载链接', reply_markup=强制回复标记)
    return REPLY


async def 添加下载任务已回复(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE) -> int:
    if await 不是主人(更新.effective_user.id):
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=await 不是主人(更新.effective_user.id))
        return ConversationHandler.END
    日志器.info(f'{更新.effective_user.name} 已回复添加下载任务')
    下载链接列表 = [更新.effective_message.text]
    try:
        async with 获取下载器() as 下载器:
            结果 = await 下载器.addUri(uris=下载链接列表)
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'已添加到下载队列: _{结果}_', parse_mode='Markdown')
    except Aria2rpcException as e:
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'添加下载任务失败,Aria2rpc异常:\n _{e}_', parse_mode='Markdown')
    except Exception as e:
        await 上下文.bot.send_message(chat_id=更新.effective_chat.id, text=f'添加下载任务失败,未知异常:\n _{e}_', parse_mode='Markdown')
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