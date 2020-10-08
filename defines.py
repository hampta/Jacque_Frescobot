from vbml import PatchedValidators
from vbml import Patcher
from tortoise import Tortoise, fields
from tortoise.models import Model
from aiogram import types
import os

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
text_pattern2 = patcher.pattern("/da <(//)*text>")


async def call():
    await Tortoise.init(db_url=str(os.getenv("CLEARDB_DATABASE_URL")),
                        modules={"models": ["__main__"]})


async def chat(message: types.Message) -> bool:
    if message.photo:
        return True


async def check(message: types.Message) -> str:
    if message.photo:
        return "message_photo"
    if message.reply_to_message and message.reply_to_message.photo:
        return "reply_photo"
    if message.reply_to_message and message.reply_to_message.sticker:
        if not message.reply_to_message.sticker.is_animated:
            return "sticker"
        else:
            return 'anim_sticker'
    else:
        return None


async def textcheck(message: types.Message):
    if text_pattern(message.text) is not None:
        text = patcher.check(message.text, text_pattern)
    elif text_pattern(message.caption) is not None:
        text = patcher.check(message.caption, text_pattern)
    else:
        return None
    return text


async def textcheck2(message: types.Message):
    if text_pattern2(message.text) is None:
        return None
    text = patcher.check(message.text, text_pattern2)
    return text

# async def check(message: types.Message) -> bool:
#    if message.reply_to_message and message.reply_to_message.photo:
#        return True

async def statistics_write(tg_chat_id):
    await call()
    info = await Event.filter(chat_id=tg_chat_id).values()
    print(info)
    if info == []:
        await Event.create(chat_id=tg_chat_id,used=0)
        used = 0
    else:
        used = info[0]['used']
    await Event.filter(chat_id=tg_chat_id).update(used=used+1)

async def statistics_read(chat_id):
    await call()
    info = await Event.filter().values()
    info_chat = await Event.filter(chat_id=chat_id).values()
    print(info_chat)
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