from aiogram import types

subscribe = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='Подписаться на рассылку')],
], resize_keyboard=True)

flats = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='Показать все варианты квартир')],
], resize_keyboard=True)
