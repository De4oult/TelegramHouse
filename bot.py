from speech_recognizer import translate
from pysondb import db

import requests as r
import funcs as f
import conf as c
import telebot


bot = telebot.TeleBot(c.token)

users = db.getDb('users.json')


@bot.message_handler(content_types=['text'])
def get_text_messages(res):
    if not users.getBy({'user' : res.from_user.id}):
        if res.text.lower() == '/start':
            bot.send_message(res.from_user.id, 'Отправьте Ваш приватный ключ')
            
        else:
            bot.send_message(res.from_user.id, f.auth(bot, res))

    else:
        if res.text.lower() == 'включи свет':
            bot.send_message(res.from_user.id, f.light_on())

        elif res.text.lower() == 'выключи свет':
            bot.send_message(res.from_user.id, f.light_off())

        elif res.text.lower()[:12] == 'поменяй цвет':
            bot.send_message(res.from_user.id, f.set_color(res.text[16:]))

        else:
            bot.send_message(res.from_user.id, 'Неизвестная команда!')

@bot.message_handler(content_types=['voice'])
def get_voice_messages(res):
    file_info = bot.get_file(res.voice.file_id)
    file_get  = r.get(f'https://api.telegram.org/file/bot{c.token}/{file_info.file_path}')

    with open(f'voices/voice_{res.from_user.id}.ogg', 'wb') as file:
        file.write(file_get.content)
    
    name_flac = f.convert_audio(f'voice_{res.from_user.id}')

    f.execute(bot, res, translate(name_flac))


bot.polling(none_stop = True, interval = 0)