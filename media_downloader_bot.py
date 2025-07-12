import logging
import re
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '7586487936:AAFd_rL6_F08GSxL7b8mKZTWhNuKVZIpojQ'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Helper functions ---

def is_tiktok_url(url):
    return 'tiktok.com' in url

def is_pinterest_url(url):
    return 'pinterest.' in url

def download_tiktok_video(url):
    # Псевдо-запрос к стороннему API (замени на рабочий)
    response = requests.get(f"https://api.tikmate.app/api/v1/download?url={url}")
    if response.status_code == 200:
        return response.json().get('video_url')
    return None

def download_pinterest_media(url):
    # Пример запроса к парсеру (может не работать, зависит от доступности сервиса)
    response = requests.post(
        'https://www.expertsphp.com/api/pinterest-downloader',
        data={'url': url}
    )
    if response.status_code == 200 and 'download_url' in response.json():
        return response.json()['download_url']
    return None

# --- Handlers ---

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Отправь ссылку на видео или фото из TikTok или Pinterest — и я скачаю его для тебя без водяных знаков!")

@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text.strip()
    if is_tiktok_url(url):
        await message.answer("⏳ Загружаю TikTok видео...")
        video_url = download_tiktok_video(url)
        if video_url:
            await bot.send_video(message.chat.id, video=video_url)
        else:
            await message.answer("❌ Не удалось скачать видео. Попробуй позже.")
    elif is_pinterest_url(url):
        await message.answer("⏳ Загружаю фото/видео с Pinterest...")
        media_url = download_pinterest_media(url)
        if media_url:
            if media_url.endswith(('.mp4', '.mov')):
                await bot.send_video(message.chat.id, video=media_url)
            else:
                await bot.send_photo(message.chat.id, photo=media_url)
        else:
            await message.answer("❌ Не удалось скачать. Попробуй другую ссылку.")
    else:
        await message.answer("⚠️ Пожалуйста, пришли ссылку на TikTok или Pinterest.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
