from bot.helper.telegram_helper.message_utils import sendMessage
from telegram.ext import run_async
from bot import AUTHORIZED_CHATS, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram.ext import Filters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import LOGGER
from bot import bot, TELEGRAM_API, TELEGRAM_HASH, USER_SESSION_STRING
from pyrogram import Client


@run_async
def authorize(update,context):
    reply_message = update.message.reply_to_message
    msg = ''
    with open('authorized_chats.txt', 'a') as file:
        if reply_message is None:
            message_args = update.message.text.split(' ')
            if len(message_args) > 1:
                user = message_args[1]
                if user not in AUTHORIZED_CHATS:
                    file.write(f'{user}\n')
                    AUTHORIZED_CHATS.add(user)
                    msg = f'User <code>{user}</code> authorized to use the bot!'
                else:
                    msg = 'User already authorized'
            else:
                # Trying to authorize a chat
                chat_id = update.effective_chat.id
                if chat_id not in AUTHORIZED_CHATS:
                    file.write(f'{chat_id}\n')
                    AUTHORIZED_CHATS.add(chat_id)
                    msg = f'Chat <code>{chat_id}</code> authorized to use the bot!'
                else:
                    msg = 'Chat already authorized'
        else:
            # Trying to authorize someone in specific
            user_id = reply_message.from_user.id
            if user_id not in AUTHORIZED_CHATS:
                file.write(f'{user_id}\n')
                AUTHORIZED_CHATS.add(user_id)
                msg = 'User <code>{user_id}</code> authorized to use the bot!'
            else:
                msg = 'User already authorized'
        sendMessage(msg, context.bot, update)


@run_async
def unauthorize(update,context):
    reply_message = update.message.reply_to_message
    if reply_message is None:
        # Trying to unauthorize a chat
        chat_id = update.effective_chat.id
        if chat_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(chat_id)
            msg = 'Chat <code>{chat_id}</code> unauthorized'
        else:
            msg = 'Already unauthorized chat'
    else:
        # Trying to authorize someone in specific
        user_id = reply_message.from_user.id
        if user_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(user_id)
            msg = 'User <code>{user_id}</code> unauthorized to use the bot!'
        else:
            msg = 'User already unauthorized!'
    with open('authorized_chats.txt', 'a') as file:
        file.truncate(0)
        for i in AUTHORIZED_CHATS:
            file.write(f'{i}\n')
    sendMessage(msg, context.bot, update)


authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)

