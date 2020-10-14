from vbml import PatchedValidators
from vbml import Patcher
from tortoise import Tortoise, fields
from tortoise.models import Model
from aiogram import types
import os
import time
from generator import classic, auto
from wand.display import display
from wand.image import Image


class Validators(PatchedValidators):
    def int(self, text: str, *args):
        valid = text.isdigit()
        if valid:
            return int(text)


class Event(Model):
    chat_id = fields.BigIntField(pk=True)
    used = fields.IntField(default=1)

    class Meta(Model):
        table = "chats"

    def __int__(self):
        return self.chat_id


patcher = Patcher(validators=Validators)
text_pattern = patcher.pattern("/dm <(//)*text>")
text_pattern2 = patcher.pattern("/liquid <ratio:int>")
text_pattern3 = patcher.pattern("/swirl <ratio>")
text_pattern4 = patcher.pattern("/wave <ratio:int> <length:int>")
text_pattern5 = patcher.pattern("/contrast <ratio:int>")
text_pattern6 = patcher.pattern("/jpeg <ratio:int>")


async def call():
    await Tortoise.init(db_url=str(os.getenv("CLEARDB_DATABASE_URL")),
                        modules={"models": ["__main__"]})


async def check(message: types.Message, file_name):
    if message.photo:
        await message.photo[-1].download(destination=file_name)
        return True
    if message.reply_to_message and message.reply_to_message.photo:
        await message.reply_to_message.photo[-1].download(destination=file_name)
        return True
    if message.reply_to_message and message.reply_to_message.sticker:
        if not message.reply_to_message.sticker.is_animated:
            await message.reply_to_message.sticker.download(destination=file_name)
            return True
        else:
            return False
    else:
        return None


async def check_dem(message: types.Message):
    if message.photo:
        return "message_photo"
    if message.reply_to_message and message.reply_to_message.photo:
        return "reply_photo"
    if message.reply_to_message and message.reply_to_message.sticker:
        if not message.reply_to_message.sticker.is_animated:
            return "sticker"
        else:
            return False
    else:
        return None


async def text_check(message: types.Message):
    if text_pattern(message.text) is not None:
        return patcher.check(message.text, text_pattern)
    elif text_pattern(message.caption) is not None:
        return patcher.check(message.caption, text_pattern)
    else:
        return None


async def text_check_liquid(message: types.Message):
    if text_pattern2(message.text) is not None:
        return patcher.check(message.text, text_pattern2)
    elif text_pattern2(message.caption) is not None:
        return patcher.check(message.caption, text_pattern2)
    else:
        return {"ratio": 35}


async def text_check_swirl(message: types.Message):
    if text_pattern3(message.text) is not None:
        return patcher.check(message.text, text_pattern3)
    elif text_pattern3(message.caption) is not None:
        return patcher.check(message.caption, text_pattern3)
    else:
        return {"ratio": 90}


async def text_check_wave(message: types.Message):
    if text_pattern4(message.text) is not None:
        return patcher.check(message.text, text_pattern4)
    elif text_pattern4(message.caption) is not None:
        return patcher.check(message.caption, text_pattern4)
    else:
        return {"ratio": 30, "length": 90}


async def text_check_contrast(message: types.Message):
    if text_pattern5(message.text) is not None:
        return patcher.check(message.text, text_pattern5)
    elif text_pattern5(message.caption) is not None:
        return patcher.check(message.caption, text_pattern5)
    else:
        return {"ratio": 100}


async def statistics_write(tg_chat_id):
    await call()
    info = await Event.filter(chat_id=tg_chat_id).values()
    if info == []:
        await Event.create(chat_id=tg_chat_id, used=0)
        used = 0
    else:
        used = info[0]['used']
    await Event.filter(chat_id=tg_chat_id).update(used=used + 1)


async def statistics_read(chat_id):
    await call()
    info = await Event.filter().values()
    info_chat = await Event.filter(chat_id=chat_id).values()
    all_used = 0
    for i in info:
        all_used += i['used']
    mes = f"Сколько бесед\Пользователей хоть раз использовало бота: " \
          f"{len(info)}\n" \
          f"Всего использований: " \
          f"{all_used}\n" \
          f"Использовалось в этом чате: " \
          f"{info_chat[0]['used']}"
    return mes


async def photo_check(message):
    file_name = f"photos/{message.chat.id}_{time.time()}.png"
    text = await text_check(message)
    attachments = await check_dem(message)
    if attachments == "message_photo":
        if text is not None:
            await message.photo[-1].download(destination=file_name)
    elif attachments == "reply_photo":
        if text is not None:
            await message.reply_to_message.photo[-1].download(destination=file_name)
    elif attachments == "sticker":
        if text is not None:
            await message.reply_to_message.sticker.download(destination=file_name)
            if text is None:
                return "А текст где"
            if len(text["text"]) == 1:
                return classic(file_name, text["text"][0])
            elif len(text["text"]) >= 2:
                return classic(file_name, text["text"][0], text["text"][1])
    elif attachments == "anim_sticker":
        return "Анимированный стикер не подходит!"
    else:
        return "А где картинка"
    if text is None:
        return
    if len(text["text"]) == 1:
        return auto(file_name, text["text"][0])
    elif len(text["text"]) >= 2:
        return auto(file_name, text["text"][0], text["text"][1])


async def liquid_photo(message):
    file_name = f"photos/{message.chat.id}_{time.time()}.png"
    text = await text_check_liquid(message)
    if await check(message, file_name):
        ratio = text['ratio'] / 100
        with Image(filename=file_name) as img:
            with img.clone() as i:
                size = i.size
                i.liquid_rescale(int(size[0] * ratio), int(size[1] * ratio))
                i.resize(size[0], size[1])
                i.save(filename=file_name)
                return file_name
    else:
        return "Нужна картинка или стикер!"


async def swirl_photo(message):
    file_name = f"photos/{message.chat.id}_{time.time()}.png"
    text = await text_check_swirl(message)
    if await check(message, file_name):
        ratio = text['ratio']
        with Image(filename=file_name) as img:
            with img.clone() as i:
                i.swirl(degree=int(ratio))
                i.save(filename=file_name)
                return file_name
    else:
        return "Нужна картинка или стикер!"


async def wave_photo(message):
    file_name = f"photos/{message.chat.id}_{time.time()}.png"
    text = await text_check_wave(message)
    if await check(message, file_name):
        ratio = text['ratio']
        length = text['length']
        with Image(filename=file_name) as img:
            with img.clone() as i:
                i.wave(ratio, length)
                i.save(filename=file_name)
                return file_name
    else:
        return "Нужна картинка или стикер!"


async def contrast_photo(message):
    file_name = f"photos/{message.chat.id}_{time.time()}.png"
    text = await text_check_contrast(message)
    if await check(message, file_name):
        ratio = text['ratio']
        with Image(filename=file_name) as img:
            with img.clone() as i:
                i.brightness_contrast(contrast=ratio)
                i.save(filename=file_name)
                return file_name
    else:
        return "Нужна картинка или стикер!"

