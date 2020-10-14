import logging
import os
import time
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile, ContentType
from defines import *
from generator import auto, classic

bot = Bot(str(os.getenv("TOKEN")))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

skip_list = ["Анимированный стикер не подходит!", "А текст где", "А где картинка", "Допустимый коэфициент от 1 до 200",
             "Недопустимый коэфициент"]

help_message = "Список команд для бота:\n" \
                "/help - помощь\n"\
                "/dm  -  Текст//текст генерирует демотиватор\n"\
                "/cas  -<коэффициент> (по стандарту  30)  Content Aware Scale, сжимает фото\n"\
                "/contrast  - <коэффициент>  (по стандарту -100) Повышение контраста\n"\
                "/swirl - <коэффициент> (по стандарту 90) Применяет эффект \"Вихрь\"\n"\
                "/wave  - <Амплитуда волны> <Размер волны> (по стандарту 30 и 90) Применяет эффект \"Волна\"\n"\
                "/stats - Статистика бота\n"\
                "Канал с демотиваторами из бота: https://t.me/Jacque_Fresco_memes"


@dp.message_handler(Command(['dm'], ignore_caption=False), content_types=[ContentType.TEXT, ContentType.PHOTO])
async def generate_modern(message: types.Message):
    try:
        photo = await photo_check(message)
        if photo in skip_list:
            await bot.send_message(chat_id=message.chat.id, text=photo)
        else:
            await bot.send_photo(chat_id=message.chat.id, photo=InputFile(photo))
            os.remove(photo)
        await statistics_write(message.chat.id)
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=f"Error код ошибки \n{e}")


@dp.message_handler(commands=["message"])
async def text_in_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=message)


@dp.message_handler(commands=["stats"])
async def text_in_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=await statistics_read(message.chat.id))


@dp.message_handler(commands=["help", "start"])
async def text_in_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=help_message)


@dp.message_handler(Command(["cas"], ignore_caption=False), content_types=[ContentType.TEXT, ContentType.PHOTO])
async def liquid(message: types.Message):
    photo = await liquid_photo(message)
    if photo in skip_list:
        await bot.send_message(chat_id=message.chat.id, text=photo)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=InputFile(photo))
        os.remove(photo)
    await statistics_write(message.chat.id)


@dp.message_handler(Command(["swirl"]),
                    content_types=[ContentType.TEXT, ContentType.PHOTO])
async def swirl(message: types.Message):
    photo = await swirl_photo(message)
    if photo in skip_list:
        await bot.send_message(chat_id=message.chat.id, text=photo)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=InputFile(photo))
        os.remove(photo)
    await statistics_write(message.chat.id)


@dp.message_handler(Command(["wave"]),
                    content_types=[ContentType.TEXT, ContentType.PHOTO])
async def swirl(message: types.Message):
    photo = await wave_photo(message)
    if photo in skip_list:
        await bot.send_message(chat_id=message.chat.id, text=photo)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=InputFile(photo))
        os.remove(photo)
    await statistics_write(message.chat.id)


@dp.message_handler(Command(["contrast"]),
                    content_types=[ContentType.TEXT, ContentType.PHOTO])
async def swirl(message: types.Message):
    photo = await contrast_photo(message)
    if photo in skip_list:
        await bot.send_message(chat_id=message.chat.id, text=photo)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=InputFile(photo))
        os.remove(photo)
    await statistics_write(message.chat.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
