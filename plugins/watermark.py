#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import shutil
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase
from helper_funcs.help_Nekmo_ffmpeg import generate_screen_shots
from helper_funcs.display_progress import progress_for_pyrogram
from import ScreenShotBot


@ScreenShotBot.on_message(Filters.private &  Filters.command("watermark"))
async def _(c, m):
    
    if not await c.db.is_user_exist(m.chat.id):
        await c.db.add_user(m.chat.id)
        await c.send_message(
            Config.LOG_CHANNEL,
            f"New User [{m.from_user.first_name}](tg://user?id={m.chat.id}) started."
        )
    
    if len(m.command) == 1:
        await m.reply_text(
            text="You can add custom watermark text to the screenshots.\n\nUsage: `/set_watermark text`. Text should not Exceed 30 characters.",
            quote=True,
            parse_mode="markdown"
        )
        return
    
    watermark_text = ' '.join(m.command[1:])
    if len(watermark_text) > 30:
        await m.reply_text(
            text=f"The watermark text you provided (__{watermark_text}__) is `{len(watermark_text)}` characters long! You cannot set watermark text greater than 30 characters.",
            quote=True,
            parse_mode="markdown"
        )
        return
    
    await c.db.update_watermark_text(m.chat.id, watermark_text)
    await m.reply_text(
        text=f"You have successfully set __{watermark_text}__ as your watermark text. From now on this will be applied to your screenshots! To remove watermark text see /settings.",
        quote=True,
        parse_mode="markdown"
    )
