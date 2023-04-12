from aioaria2 import Aria2rpcException
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from ..下载器 import 获取下载器
from ..小工具 import (
    不是主人,
    仅主人装饰器,
    有机体可读下载任务详细结果,
)
from ..日志 import 日志器

REPLY = range(1)


async def 操作单任务回复中(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    强制回复标记 = ForceReply(selective=True, input_field_placeholder="请输入任务ID")
    await 上下文.bot.send_message(
        chat_id=更新.effective_chat.id,
        text="请输入任务ID",
        reply_markup=强制回复标记,
        reply_to_message_id=更新.effective_message.id,
    )
    return REPLY


操作单任务内联键盘 = [
    [
        InlineKeyboardButton("暂停", callback_data="暂停单任务"),
        InlineKeyboardButton("继续", callback_data="继续单任务"),
    ],
    [InlineKeyboardButton("删除", callback_data="删除单任务")],
    [
        InlineKeyboardButton("刷新", callback_data="刷新单任务"),
        InlineKeyboardButton("返回", callback_data="回主菜单"),
    ],
]
操作单任务回复标记 = InlineKeyboardMarkup(操作单任务内联键盘)


async def 操作单任务回复(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    不是主人旗 = await 不是主人(更新.effective_user.id)
    if 不是主人旗:
        await 上下文.bot.send_message(
            chat_id=更新.effective_chat.id,
            text=不是主人旗,
            reply_to_message_id=更新.effective_message.id,
        )
        return ConversationHandler.END
    日志器.info(f"{更新.effective_user.name} 请求操作单任务 {更新.effective_message.text}")
    任务id = 更新.effective_message.text
    上下文.user_data["任务id"] = 任务id
    try:
        async with 获取下载器() as 下载器:
            任务状态 = await 下载器.tellStatus(任务id)
        好任务状态 = await 有机体可读下载任务详细结果(任务状态)
        await 上下文.bot.send_message(
            chat_id=更新.effective_chat.id,
            text=好任务状态,
            parse_mode="Markdown",
            reply_markup=操作单任务回复标记,
            reply_to_message_id=更新.effective_message.id,
        )
    except Exception as e:
        await 上下文.bot.send_message(
            chat_id=更新.effective_chat.id,
            text=f"操作失败,未知异常:\n _{e}_",
            parse_mode="Markdown",
            reply_to_message_id=更新.effective_message.id,
        )
    finally:
        return ConversationHandler.END


操作单任务对话处理器 = ConversationHandler(
    per_chat=True,
    per_user=True,
    entry_points=[MessageHandler(filters.Regex("操作单任务"), 操作单任务回复中)],
    states={
        REPLY: [MessageHandler(~filters.COMMAND, 操作单任务回复)],
    },
    fallbacks=[MessageHandler(~filters.COMMAND, 操作单任务回复)],
    allow_reentry=True,
)


@仅主人装饰器
async def 暂停单任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    任务id = 上下文.user_data["任务id"]
    日志器.info(f"{更新.effective_user.name} 请求暂停单任务 {任务id}")
    try:
        async with 获取下载器() as 下载器:
            await 下载器.pause(任务id)
            新任务状态 = await 下载器.tellStatus(任务id)
        新好任务状态 = await 有机体可读下载任务详细结果(新任务状态)
        await 上下文.bot.edit_message_text(
            chat_id=更新.effective_chat.id,
            message_id=更新.callback_query.message.id,
            text=f"{新好任务状态}\n 已暂停任务",
            parse_mode="Markdown",
            reply_markup=操作单任务回复标记,
        )
    except Aria2rpcException:
        pass
    except Exception as e:
        日志器.error(f"暂停单任务失败: {e}")
        await 上下文.bot.send_message(
            chat_id=更新.effective_chat.id,
            text=f"操作失败,未知异常:\n _{e}_",
            parse_mode="Markdown",
            reply_to_message_id=更新.effective_message.id,
        )


@仅主人装饰器
async def 继续单任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    任务id = 上下文.user_data["任务id"]
    日志器.info(f"{更新.effective_user.name} 请求继续单任务 {任务id}")
    try:
        async with 获取下载器() as 下载器:
            await 下载器.unpause(任务id)
            新任务状态 = await 下载器.tellStatus(任务id)
        新好任务状态 = await 有机体可读下载任务详细结果(新任务状态)
        await 上下文.bot.edit_message_text(
            chat_id=更新.effective_chat.id,
            message_id=更新.callback_query.message.id,
            text=f"{新好任务状态}\n 已继续任务",
            parse_mode="Markdown",
            reply_markup=操作单任务回复标记,
        )
    except Aria2rpcException:
        pass
    except Exception as e:
        日志器.error(f"继续单任务失败: {e}")
        await 上下文.bot.send_message(
            chat_id=更新.effective_chat.id,
            text=f"操作失败,未知异常:\n _{e}_",
            parse_mode="Markdown",
            reply_to_message_id=更新.effective_message.id,
        )


删除单任务回复标记 = InlineKeyboardMarkup([[InlineKeyboardButton("返回", callback_data="回主菜单")]])


@仅主人装饰器
async def 删除单任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    任务id = 上下文.user_data["任务id"]
    日志器.info(f"{更新.effective_user.name} 请求删除单任务 {任务id}")
    try:
        async with 获取下载器() as 下载器:
            await 下载器.remove(任务id)
        await 上下文.bot.edit_message_text(
            chat_id=更新.effective_chat.id,
            message_id=更新.callback_query.message.id,
            text="已删除任务",
            parse_mode="Markdown",
            reply_markup=删除单任务回复标记,
        )
    except Exception as e:
        日志器.error(f"删除单任务失败: {e}")
        await 上下文.bot.send_message(
            chat_id=更新.effective_chat.id,
            text=f"操作失败,未知异常:\n _{e}_",
            parse_mode="Markdown",
            reply_to_message_id=更新.effective_message.id,
        )


@仅主人装饰器
async def 刷新单任务(更新: Update, 上下文: ContextTypes.DEFAULT_TYPE):
    任务id = 上下文.user_data["任务id"]
    日志器.info(f"{更新.effective_user.name} 请求刷新单任务 {任务id}")
    try:
        async with 获取下载器() as 下载器:
            任务状态 = await 下载器.tellStatus(任务id)
        好任务状态 = await 有机体可读下载任务详细结果(任务状态)
        await 上下文.bot.edit_message_text(
            chat_id=更新.effective_chat.id,
            message_id=更新.callback_query.message.id,
            text=f"{好任务状态}",
            parse_mode="Markdown",
            reply_markup=操作单任务回复标记,
        )
    except BadRequest:
        await 上下文.bot.edit_message_text(
            chat_id=更新.effective_chat.id,
            message_id=更新.callback_query.message.id,
            text=f"{好任务状态}\n_当前状态无变化_",
            parse_mode="Markdown",
            reply_markup=操作单任务回复标记,
        )
    except Exception as e:
        日志器.error(f"刷新单任务失败: {e}")
        await 上下文.bot.send_message(
            chat_id=更新.effective_chat.id,
            text=f"操作失败,未知异常:\n _{e}_",
            parse_mode="Markdown",
            reply_to_message_id=更新.effective_message.id,
        )


暂停单任务处理器 = CallbackQueryHandler(暂停单任务, pattern="暂停单任务")
继续单任务处理器 = CallbackQueryHandler(继续单任务, pattern="继续单任务")
删除单任务处理器 = CallbackQueryHandler(删除单任务, pattern="删除单任务")
刷新单任务处理器 = CallbackQueryHandler(刷新单任务, pattern="刷新单任务")
