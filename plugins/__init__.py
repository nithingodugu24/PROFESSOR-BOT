from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums 
from database.users_chats_db import db
from info import SUPPORT_CHAT,UPTIME
from aiohttp import web
from datetime import datetime
import asyncio, re, ast, time, math, logging, random, os, pyrogram, shutil, psutil 
import pytz

import json
# Helper Function
from Script import script
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink, get_time, humanbytes 
from .ExtraMods.carbon import make_carbon
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, PICS, IMDB, PM_IMDB, SINGLE_BUTTON, PROTECT_CONTENT, \
    SPELL_CHECK_REPLY, IMDB_TEMPLATE, IMDB_DELET_TIME, START_MESSAGE, PMFILTER, G_FILTER, BUTTON_LOCK, BUTTON_LOCK_TEXT, SHORT_URL, SHORT_API

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response(text='{"status":"running","dev":"hasiba518738"}')

@routes.get("/helloWorld", allow_head=True)
async def root_route_handler(request):
    return web.json_response(text='{"success":true,"message":"Hello World !"}')

@routes.get("/serverStatistics", allow_head=True)
async def server_statistics_handler(request):
    current_utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    epoch_utc_time = datetime.utcfromtimestamp(UPTIME).replace(tzinfo=pytz.utc)
    time_difference = current_utc_time - epoch_utc_time
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    services = [process for process in psutil.process_iter(['pid', 'name']) if process.info['name'].lower() == 'services.exe']
    num_services = len(services)
    minutes, seconds = divmod(remainder, 60)
    num_threads = psutil.cpu_count(logical=False)  # Physical CPU cores
    num_processes = psutil.cpu_count(logical=True)  # Total CPU cores including hyper-threading

    total, used, free = shutil.disk_usage(".")
    stats = {
        "uptime": f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds" ,
        "startedAt": UPTIME,
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "total_disk_space": humanbytes(total),
        "used_disk_space": humanbytes(used),
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "free_disk_space": humanbytes(free),
        "num_services": num_services,
        "num_threads": num_threads,
        "num_processes": num_processes,
    }
    return web.json_response(text=json.dumps(stats))

# Remove the duplicated web_server() function
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
