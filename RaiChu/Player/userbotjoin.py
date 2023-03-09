import asyncio
from RaiChu.config import BOT_USERNAME, SUDO_USERS
from Process.decorators import authorized_users_only, sudo_users_only, errors
from Process.filters import command, other_filters
from Process.main import user as USER
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except BaseException:
        await message.reply_text(
            "• **من مۆڵەتم نییە:**\n\n» ❌ __زیادکردنی بە کارهێنە ر__",
        )
        return

    try:
        user = await USER.get_me()
    except BaseException:
        user.first_name = "یاریدەدەری مۆسیقا"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 Flood Wait Error 🛑 \n\n**userbot couldn't بەشداری گروپەکەت بکە بەهۆی زۆری داواکاری بەشداریکردن بۆ**"
            "\n\n**یان بە دەستی یاریدەدەر زیاد بکە بۆ گروپەکەت و دووبارە هەوڵبدەرەوە**",
        )
        return
    await message.reply_text(
        f"** بە سەرکەوتوویی چووە ناو چاتەو**",
    )


@Client.on_message(command(["userbotleave",
                            f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def leave_one(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ بە سەرکەوتوویی چاتی جێهێشت")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "❌ **نەیتوانی گروپەکەت بەجێبهێڵێت، لەوانەیە Floodwaits بێت.**\n\n**» یان بە دەستی لە گروپەکەتەوە لێبدە**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **بەکارهێنەر بۆت** جێهێشتنی هەموو چاتەکان !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f" جێهێشتنی هەموو گروپێک...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"ڕۆشتن...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ بە سە ەکە وتووی رۆشت: {left} chats.\n❌ Failed in: {failed} chats."
    )
