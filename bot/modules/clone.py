from telegram.ext import CommandHandler
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import new_thread
from bot import dispatcher


@new_thread
def cloneNode(update,context):
    args = update.message.text.split(" ",maxsplit=1)
    tag = update.message.from_user.username
    if len(args) > 1:
        link = args[1]
        msg = sendMessage(f"✨ Cloning: <code>{link}</code>",context.bot,update)
        gd = GoogleDriveHelper()
        result = gd.clone(link)
        deleteMessage(context.bot,msg)
        text = result[0]
        markup = result[1]
        text += f'\n\ncc: @{tag}'
        sendMessageMarkup(text,markup,context.bot,update)
    else:
        sendMessage("⚠ Provide Google Drive Shareable Link to Clone.",context.bot,update)

clone_handler = CommandHandler(BotCommands.CloneCommand,cloneNode,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(clone_handler)