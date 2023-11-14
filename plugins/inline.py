import logging
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InlineQuery,InputTextMessageContent
from database.ia_filterdb import get_search_results
from utils import is_subscribed, get_size, temp
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
import requests

async def get_imdb_data(user_text, offset = 0):
    base_url = "https://v3.sg.media-imdb.com/suggestion/titles/x/"
    url = f"{base_url}{user_text}.json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        shows = data.get("d", [])
        if offset < len(shows):
            return shows, offset+ len(shows)

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

async def inline_users(query: InlineQuery):
    if AUTH_USERS:
        if query.from_user and query.from_user.id in AUTH_USERS:
            return True
        else:
            return False
    if query.from_user and query.from_user.id not in temp.BANNED_USERS:
        return True
    return False
@Client.on_inline_query()
async def answer(bot, query):
    if not await inline_users(query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='okDa',
                           switch_pm_parameter="hehe")
        return

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='You have to subscribe my channel to use the bot',
                           switch_pm_parameter="subscribe")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    #files, next_offset, total = await get_search_results(string, file_type=file_type, max_results=10, offset=offset)
    movies,next_offset  = await get_imdb_data(string,offset=offset)
    total = len(movies)
    for file in movies:
        button = InlineKeyboardButton("button_text", callback_data="button_callback")
        buttons = [
            [
                InlineKeyboardButton("Next", callback_data=f"next_{offset}"),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)
        results.append(
            InlineQueryResultArticle(
                id=file.get("id", "100"),
                title=file.get("l", "no text"),
                input_message_content=InputTextMessageContent(file.get("l", "")),
                description=file.get("s", "No actors disclosed !"),
                thumb_url=file.get("i", {}).get("imageUrl", "https://graph.org/file/a6bb16181880bcb6d2435.jpg"),
                thumb_height = int(file.get("i", {}).get("height", 700)),
                thumb_width = int(file.get("i", {}).get("width", 500))
            )
        )

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Trending Movies - {total}"
        if string:
            switch_pm_text += f" for {string}"

        # Update next_offset based on the current offset and the number of results
        next_offset = offset + len(results)

        try:
            await query.answer(results=results,
                               is_personal=True,
                               cache_time=cache_time,
                               switch_pm_text=switch_pm_text,
                               switch_pm_parameter="start",
                               next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No Results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal=True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")

# ... (remaining code)
def get_reply_markup(query):
    buttons = [[InlineKeyboardButton('⟳ ꜱᴇᴀʀᴄʜ ᴀɢᴀɪɴ', switch_inline_query_current_chat=query)]]
    return InlineKeyboardMarkup(buttons)



