from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#1
button_prog_lang = KeyboardButton(text='/Progr_langs')
b_read_me = KeyboardButton(text='/Read_me')
b_download = KeyboardButton(text='/Download')
b_show = KeyboardButton(text='/Show')
b_cur = KeyboardButton(text='/Info')
b_about = KeyboardButton(text='/About')

#2
b_python = KeyboardButton(text='/Python')
b_cpp = KeyboardButton(text='/C++')
b_java = KeyboardButton(text='/Java')
b_php = KeyboardButton(text='/PHP')
b_back = KeyboardButton(text='/<Back')

main_keyboard = ReplyKeyboardMarkup(keyboard=[[button_prog_lang, b_read_me, b_download],
                                              [b_show, b_cur, b_about]], resize_keyboard=True)

sec_keyboard = ReplyKeyboardMarkup(keyboard=[[b_python, b_cpp], [b_java, b_php], [b_back]], resize_keyboard=True)
