from bot.helper.telegram_helper.message_utils import sendMessage
from telegram.ext import run_async
from bot import AUTHORIZED_CHATS, dispatcher, LOGGER
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram.ext import Filters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands


@run_async
def authorize(update,context):
    reply_message = update.message.reply_to_message
    message_args = update.message.text.split(' ')
    msg = ''
    with open('authorized_chats.txt', 'a') as file:
        if reply_message is None and len(message_args) < 1:
            # Trying to authorize a chat
            chat_id = update.effective_chat.id
            if chat_id not in AUTHORIZED_CHATS:
                file.write(f'{chat_id}\n')
                AUTHORIZED_CHATS.add(chat_id)
                msg = f'Chat {chat_id}authorized'
                LOGGER.info(f'Chat {chat_id} authorized')
            else:
                msg = f'Already authorized chat {chat_id}'
        else:
            # Trying to authorize someone in specific
            if len(message_args) > 1:
                user_id = int(message_args[1])
            else:
                user_id = reply_message.from_user.id
            if user_id not in AUTHORIZED_CHATS:
                file.write(f'{user_id}\n')
                AUTHORIZED_CHATS.add(user_id)
                msg = f'Person {user_id} Authorized to use the bot!'
                LOGGER.info(f'Person {user_id} authorized')
            else:
                msg = f'Person {user_id} already authorized'
        sendMessage(msg, context.bot, update)


@run_async
def unauthorize(update,context):
    reply_message = update.message.reply_to_message
    message_args = update.message.text.split(' ')
    if reply_message is None and len(message_args) < 1:
        # Trying to unauthorize a chat
        chat_id = update.effective_chat.id
        if chat_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(chat_id)
            msg = f'Chat {chat_id} unauthorized'
            LOGGER.info(f'Chat {chat_id} unauthorized')
        else:
            msg = 'Already unauthorized chat'
    else:
        # Trying to authorize someone in specific
        if len(message_args) > 1:
            user_id = message_args[1]
        else:
            user_id = reply_message.from_user.id
        if user_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(user_id)
            msg = f'Person {user_id} unauthorized to use the bot!'
        else:
            msg = 'Person already unauthorized!'
    with open('authorized_chats.txt', 'a') as file:
        file.truncate(0)
        for i in AUTHORIZED_CHATS:
            file.write(f'{i}\n')
    sendMessage(msg, context.bot, update)


authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter & (Filters.group | Filters.private))
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter & (Filters.group | Filters.private))
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)

