from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums 
from database.users_chats_db import db
from info import SUPPORT_CHAT
from aiohttp import web
from utils import temp
import logging, re, asyncio, time, shutil, psutil, os, sys
from datetime import datetime
import json
# Helper Function
from Script import script
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink, get_time, humanbytes 
from .ExtraMods.carbon import make_carbon
import info

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response(text='{"status":"running","dev":"hasiba518738"}')

@routes.get("/helloWorld", allow_head=True)
async def root_route_handler(request):
    return web.json_response(text='{"success":true,"message":"Hello World !"}')

@routes.get("/serverStatistics", allow_head=True)
async def root_route_handler(request):
    return web.json_response(text='{"success":true,"message":"Hello World !"}')


@routes.get("/serverStatistics", allow_head=True)
async def server_statistics_handler(request):
    total, used, free = shutil.disk_usage(".")
    stats = {
        "uptime": get_time(time.time() - info.UPTIME),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "total_disk_space": humanbytes(total),
        "used_disk_space": humanbytes(used),
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "free_disk_space": humanbytes(free)
    }
    return web.json_response(text=json.dumps(stats))

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def banned_users(_, client, message: Message):
    return (message.from_user is not None or not message.sender_chat) and (message.from_user.id in temp.BANNED_USERS)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

@Client.on_message(filters.private & filters.incoming & filters.create(banned_users))
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f"Sᴏʀʀʏ Dᴜᴅᴇ, Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ Tᴏ Usᴇ Mᴇ. \nBᴀɴ Rᴇᴀsᴏɴ: {ban['ban_reason']}")

@Client.on_message(filters.group & filters.incoming & filters.create(disabled_chat))
async def grp_bd(bot, message):
    buttons = [[InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ', url=f'https://t.me/{SUPPORT_CHAT}')]]
    chat = await db.get_chat(message.chat.id)
    k = await message.reply(text=f"CHAT NOT ALLOWED 🐞\n\nMʏ Aᴅᴍɪɴs Hᴀs Rᴇsᴛʀɪᴄᴛᴇᴅ Mᴇ Fʀᴏᴍ Wᴏʀᴋɪɴɢ Hᴇʀᴇ ! Iғ Yᴏᴜ Wᴀɴᴛ Tᴏ Kɴᴏᴡ Mᴏʀᴇ Aʙᴏᴜᴛ Iᴛ Cᴏɴᴛᴀᴄᴛ Sᴜᴘᴘᴏʀᴛ..\nRᴇᴀꜱᴏɴ : <code>{chat['reason']}</code>.", reply_markup=InlineKeyboardMarkup(buttons))
    try: await k.pin()
    except: pass
    await bot.leave_chat(message.chat.id)
