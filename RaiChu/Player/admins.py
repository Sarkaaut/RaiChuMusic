from Process.Cache.admins import admins
from Process.main import call_py
from pyrogram import filters
from Process.decorators import authorized_users_only
from Process.filters import command, other_filters
from Process.queues import QUEUE, clear_queue
from Process.main import bot as Client
from Process.utils import skip_current_song, skip_item
from RaiChu.config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL, IMG_5
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from RaiChu.inline import stream_markup

bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 بڕۆ بۆ دواوە", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 داخستن", callback_data="cls")]]
)


@Client.on_message(command(["دووبارە بارکردنەوە", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="کارگێڕان")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅بۆت ** بە دروستی بارکرایەوە!**\n✅ ** لیستی ئەدمینەکان** هەیەتی ** نوێکراوەتەوە!**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• Mᴇɴᴜ", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• Cʟᴏsᴇ", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ لە ئێستادا هیچ شتێک كار ناکات")
        elif op == 1:
            await m.reply("✅ __ ڕیزەکان__ ** به‌تاڵه‌.**\n\n**• جێهێشتنی چاتی دەنگی**")
        elif op == 2:
            await m.reply("🗑️ ** پاککردنەوەی نزیکییەکان**\n\n**• جێهێشتنی چاتی دەنگی**")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ ** پەڕینەوە بۆ تراکی داهاتوو.**\n\n🏷 ** ناو:** [{op[0]}]({op[1]})\n💭 ** چات:** `{chat_id}`\n💡 ** دۆخ:** `ئیش پی کردن`\n🎧 ** داواکاری لەلایەن:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 ** گۆرانی لە نزیکی لابرا:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ پەیوەندی لە ڤیدیۆ چاتی پچڕاوە.")
        except Exception as e:
            await m.reply(f"🚫 ** هەڵە:**\n\n`{e}`")
    else:
        await m.reply("❌ ** هیچ شتێک ستریم نییە**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ ** تراک وەستا.**\n\n• ** بۆ دەستپێکردنەوەی ستریمەکە، بەکارهێنانی...**\n» /resume command."
            )
        except Exception as e:
            await m.reply(f"🚫 **هەڵە:**\n\n`{e}`")
    else:
        await m.reply("❌ **nothing in streaming**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **تراک دەستی پێکردەوە.**\n\n• **بۆ وەستاندنی سترێمەکە، بەکارهێنانی**\n» /pause command."
            )
        except Exception as e:
            await m.reply(f"🚫 **هەڵە:**\n\n`{e}`")
    else:
        await m.reply("❌ **هیچ لە ستریمینگدا نییە**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **بێدەنگ کراوە.**\n\n• **بۆ لابردنی بێدەنگی بەکارهێنەر، بەکارهێنانی**\n» /فەرمانی unmute."
            )
        except Exception as e:
            await m.reply(f"🚫 **هەڵە:**\n\n`{e}`")
    else:
        await m.reply("❌ **هیچ لە ستریمینگدا نییە**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **بێدەنگ نەکراوە.**\n\n• **بۆ بێدەنگکردنی، بەکارهێنانی**\n» /mute فەرمان."
            )
        except Exception as e:
            await m.reply(f"🚫 **هەڵە:**\n\n`{e}`")
    else:
        await m.reply("❌ **هیچ لە ستریمینگدا نییە**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("تۆ ئەدمینێکی بێناویت !\n\n» گەڕانەوە بۆ ئەکاونتی بەکارهێنەر لە مافی بەڕێوەبەرەوە.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 تەنها ئەدمینێک کە مۆڵەتی بەڕێوەبردنی چاتی دەنگی هەیە کە دەتوانێت ئەم دوگمەیە لێبدات !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ ستریمینگ وەستاوە", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **هەڵە:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لە ئێستادا هیچ شتێک Streaming نییە", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("تۆ ئەدمینێکی بێناویت !\n\n» گەڕانەوە بۆ ئەکاونتی بەکارهێنەر لە مافی بەڕێوەبەرەوە.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 تەنها ئەدمینێک کە مۆڵەتی بەڕێوەبردنی چاتی دەنگی هەیە کە دەتوانێت ئەم دوگمەیە لێبدات !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ ستریمینگ دەستی پێکردەوە", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **هەڵە:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لە ئێستادا هیچ شتێک Streaming نییە", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("تۆ ئەدمینێکی بێناویت !\n\n» گەڕانەوە بۆ ئەکاونتی بەکارهێنەر لە مافی بەڕێوەبەرەوە.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 تەنها ئەدمینێک کە مۆڵەتی بەڕێوەبردنی چاتی دەنگی هەیە کە دەتوانێت ئەم دوگمەیە لێبدات !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **ئەم ستریمینگە کۆتایی هات**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **هەڵە:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لە ئێستادا هیچ شتێک Streaming نییە", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("تۆ ئەدمینێکی بێناویت !\n\n» گەڕانەوە بۆ ئەکاونتی بەکارهێنەر لە مافی بەڕێوەبەرەوە.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 تەنها ئەدمینێک کە مۆڵەتی بەڕێوەبردنی چاتی دەنگی هەیە کە دەتوانێت ئەم دوگمەیە لێبدات !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 بە سەرکەوتوویی بێدەنگ کرا", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **هەڵە:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لە ئێستادا هیچ شتێک Streaming نییە", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("تۆ ئەدمینێکی بێناویت !\n\n» گەڕانەوە بۆ ئەکاونتی بەکارهێنەر لە مافی بەڕێوەبەرەوە.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 تەنها ئەدمینێک کە مۆڵەتی بەڕێوەبردنی چاتی دەنگی هەیە کە دەتوانێت ئەم دوگمەیە لێبدات !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 بە سەرکەوتوویی بێدەنگ نەکرا", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **هەڵە:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لە ئێستادا هیچ شتێک لە ستریمدا نییە", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **دەنگی دانراو** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **هەڵە:**\n\n`{e}`")
     
        await m.reply("❌ **هیچ لە ستریمینگدا نییە**")

@Client.on_callback_query(filters.regex("cbskip"))
async def cbskip(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 تەنها ئەدمینێک کە مۆڵەتی manage video chat ی هەیە کە دەتوانێت ئەم دوگمەیە لێبدات !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    queue = await skip_current_song(chat_id)
    if queue == 0:
        await query.answer("❌ هیچ شتێک لە ئێستادا كار ناکات", show_alert=True)
    elif queue == 1:
        await query.answer("» ئیتر هیچ میوزیکێک لە Queue بۆ Skip نییە، ڤیدیۆ چاتی بەجێدەهێڵێت.", show_alert=True)
    elif queue == 2:
        await query.answer("🗑️ Clearing the **Queues**\n\n» **Bot Music Kurdish** جێهێشتنی ڤیدیۆ چات.", show_alert=True)
    else:
        await query.answer("goes to the next track, proccessing...")
        await query.message.delete()
        buttons = stream_markup(user_id)
        requester = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})"
        thumbnail = f"{IMG_5}"
        title = f"{queue[0]}"
        userid = query.from_user.id
        gcname = query.message.chat.title
        ctitle = await CHAT_TITLE(gcname)
        image = await thumb(thumbnail, title, userid, ctitle)
        await _.send_photo(
            chat_id,
            photo=image,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"⏭ ** بۆ تراکی داهاتوو.\n\n🗂 **ناو:** [{queue[0]}]({queue[1]})\n💭 **چات:** `{chat_id}`\n🧸 **داواکاری لەلایەن:** {requester}",
        )
        remove_if_exists(image)
