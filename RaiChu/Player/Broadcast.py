import asyncio

from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant

from Process.main import bot as Ufo
from RaiChu.config import SUDO_USERS

@Client.on_message(filters.command(["gcast"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("`دەستپێکردنی پەخش...`")
        if not message.reply_to_message:
            await wtf.edit("تکایە وەڵامی نامەیەک بدەنەوە بۆ دەستپێکردنی پەخش!")
            return
        lmao = message.reply_to_message.text
        async for dialog in Ufo.iter_dialogs():
            try:
                await Ufo.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`پەخش کردن...` \n\n** نێردراوە بۆ:** `{sent}` chats \n** شکستی هێنا لە:** {failed} chats")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_text(f"`  بە سەرکەوتوویی كارا كرا` \n\n** نێردراوە بۆ:** `{sent}` chats \n** شکستی هێنا لە:** {failed} chats")
