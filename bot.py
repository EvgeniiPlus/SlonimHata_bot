import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import LinkPreviewOptions
from dotenv import load_dotenv

from db import Database, Flat
import keyboards
from parse import get_flats

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        'Привет! Выбери действие для продолжения...',
        reply_markup=keyboards.flats,
    )


@dp.message(F.text == 'Показать все варианты квартир')
async def show_all_flats(message: types.Message):
    get_flats()
    db = Database()
    all_flats = db.get_all(Flat)
    await message.answer(f'Найдено {len(all_flats)} квартир')
    for flat in all_flats:
        message_text = (
            f'🏠 Адрес: {flat.address}\n\n'
            f'📝 Описание: {flat.description}\n\n'
            f'<b>💰 Цена: {flat.price}</b>\n\n'
            f'<a href="{flat.link}">🔗 Смотреть объявление</a>'
        )
        if flat.img_link:
            await message.answer_photo(
                photo=flat.img_link,
                caption=message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.flats,
            )
        else:
            await message.answer(
                text='<i>Нет фотографий</i>😔\n\n' + message_text,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                parse_mode=ParseMode.HTML,
                reply_markup=keyboards.flats,
            )
        await asyncio.sleep(0.5)


@dp.message(F.text == 'Показать новые варианты')
async def show_new_flats(message: types.Message):
    new_flats = get_flats()
    await message.answer(f'Найдено {len(new_flats)} новых квартир')
    for flat in new_flats:
        message_text = (
            f'🏠 Адрес: {flat["address"]}\n\n'
            f'📝 Описание: {flat["description"]}\n\n'
            f'<b>💰 Цена: {flat["price"]}</b>\n\n'
            f'<a href="{flat["link"]}">🔗 Смотреть объявление</a>'
        )
        await message.answer(
            text=message_text,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.flats,
        )
        await asyncio.sleep(0.5)


async def scheduled_messages():
    while True:
        await asyncio.sleep(10)

        new_flats = get_flats()
        users = [user.strip() for user in os.getenv('USERS').split(',')]
        for user in users:
            try:
                if new_flats:
                    for flat in new_flats:
                        message_text = (
                            f'🥳 <b>НОВАЯ КВАРТИРА В СЛОНИМЕ</b> 🥳\n\n'
                            f'🏠 Адрес: {flat["address"]}\n\n'
                            f'📝 Описание: {flat["description"]}\n\n'
                            f'<b>💰 Цена: {flat["price"]}</b>\n\n'
                            f'<a href="{flat["link"]}">🔗 Смотреть объявление</a>'
                        )
                        if flat["img_link"]:
                            await bot.send_photo(
                                chat_id=user,
                                photo=flat["img_link"],
                                caption=message_text,
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboards.flats,
                            )
                        else:
                            await bot.send_message(
                                chat_id=user,
                                text='<i>Нет фотографий</i>😔\n\n' + message_text,
                                link_preview_options=LinkPreviewOptions(is_disabled=True),
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboards.flats,
                            )
            except Exception as e:
                logging.error(f"Ошибка при отправке сообщения пользователю {user}: {e}")


async def main():
    asyncio.create_task(scheduled_messages())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
