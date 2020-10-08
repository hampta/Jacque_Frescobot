import logging
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile, ContentType
from defines import *
from generator import auto, classic

bot = Bot(str(os.getenv("TOKEN")))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

help_message = "Список команд для бота:\n" \
               "Генерация демотиватора из приклеплённой картинки\n" \
               "или в ответ на сообщение с картинкой или стикером:\n" \
               "/dm Верхний текст//нижний текст(опционально)\n" \
               "Канал с демотиваторами из бота: https://t.me/Jacque_Fresco_memes"



@dp.message_handler(commands=["dm"])
async def generate_modern(message: types.Message):
    try:
        file_name = f"photos/{message.chat.id}_{time.time()}.png"
        textch = await textcheck(message)
        attachments = await check(message)
        if attachments == "message_photo":
            if textch is not None:
                await message.photo[-1].download(destination=file_name)
        elif attachments == "reply_photo":
            if textch is not None:
                await message.reply_to_message.photo[-1].download(destination=file_name)
        elif attachments == "sticker":
            if textch is not None:
                await message.reply_to_message.sticker.download(destination=file_name)
                if textch is None:
                    return
                if len(textch["text"]) == 1:
                    media = InputFile(classic(file_name, textch["text"][0]))
                elif len(textch["text"]) >= 2:
                    media = InputFile(classic(file_name, textch["text"][0], textch["text"][1]))
                await bot.send_photo(chat_id=message.chat.id, photo=media, reply_to_message_id=message.message_id)
                os.remove(file_name)
                await statistics_write(message.chat.id)
                return
        elif attachments == "anim_sticker":
            await bot.send_message(chat_id=message.chat.id, text=f"Анимированный стикер не подходит!")
        else:
            await bot.send_message(chat_id=message.chat.id, text=f"А где картинка")
            return
        if textch is None:
            return
        if len(textch["text"]) == 1:
            media = InputFile(auto(file_name, textch["text"][0]))
        elif len(textch["text"]) >= 2:
            media = InputFile(auto(file_name, textch["text"][0], textch["text"][1]))
        await bot.send_photo(chat_id=message.chat.id, photo=media, reply_to_message_id=message.message_id)
        os.remove(file_name)
        await statistics_write(message.chat.id)
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=f"ERROR код ошибки \n{e}")


@dp.message_handler(commands=["message"])
async def text_in_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=message)


@dp.message_handler(commands=["stats"])
async def text_in_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=await statistics_read(message.chat.id))


@dp.message_handler(commands=["help", "start"])
async def text_in_handler(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=help_message)


if __name__ == '__main__':
    print("Бот запущен!")
    executor.start_polling(dp, skip_updates=True)
