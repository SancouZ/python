import asyncio
import logging
import sys
import json
from os import getenv
from rapidfuzz import process, fuzz

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


TOKEN = "7925704990:AAHPYvUmNVg8YETSUIwgCLVOO9CfFCGyNmk"


dp = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message, bot) -> None:
    print(message.text)
    print(message.message_thread_id)

    with open('keywords.json', encoding='utf8') as file:
        data = json.load(file)
        
    
    # with open('configbot.json') as file:
    #     data = json.load(file)
    #     print(data.name)

# Строка, которую нужно сравнить с ключевыми словами
    input_string = message.text

# Инициализация переменных для хранения лучшего совпадения
    best_match = None
    best_score = 0
    best_type = None

# Проход по каждому объекту в массиве
    for item in data:
        keywords = item["keywords"]
        type_ = item["type"]
    
    # Поиск наиболее похожего ключевого слова в текущем объекте
        match = process.extractOne(input_string, keywords, scorer=fuzz.ratio)
    
    # Если найденное совпадение лучше предыдущих, обновляем лучшее совпадение
        if match[1] > best_score:
            best_match = match[0]
            best_score = match[1]
            best_type = type_

# Вывод результата
    if best_match:
        print(f"Наиболее похожее ключевое слово: {best_match}")
        print(f"Сходство: {best_score}%")
        print(f"Тип: {best_type}")
    else:
        print("Совпадений не найдено.")

    resptime = 180
    if message.message_thread_id == 669: 
        resptime = 90
    else:
        resptime = 180 

    response = f"Ответим в течении {resptime} минут {best_type}"   
    if best_score < 60:
        return 
    
    try: 
        await bot.send_message(chat_id=message.chat.id, text=response,  message_thread_id=message.message_thread_id)
    except TypeError:
        await bot.send_message(chat_id=message.chat.id, text="Ошибка",  message_thread_id=message.message_thread_id)

async def main(bot) -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls


    with open('configbot.json', encoding='utf8') as file:
        data = json.load(file)
        print(data[0]["name"])


    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(bot))



