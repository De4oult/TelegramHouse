from conf import private_key
from fuzzywuzzy import fuzz
from include import device
from pysondb import db

import subprocess as sp
import os

users = db.getDb('users.json')

def auth(bot, res) -> bool:
    if res.text.lower() == private_key:
        users.add({'user' : res.from_user.id})
        bot.send_message(res.from_user.id, 'Теперь Вы можете управлять домом')

    else:
        bot.send_message(res.from_user.id, 'Неправильный приватный ключ!')
              

def light_on() -> str:
    device.turn_on()
    return 'Включаю свет'

def light_off() -> str:
    device.turn_off()
    return 'Выключаю свет'

def set_color(colour: str) -> str:
    colours = {
        'красный'    : (255, 0, 0),
        'зелёный'    : (0, 128, 0),
        'синий'      : (0, 0, 255),
        'фиолетовый' : (148, 0, 211),
        'желтый'     : (255, 255, 0),
        'белый'      : (255, 255, 255)
    }

    color = colours[colour]

    device.set_colour(color[0], color[1], color[2])

    return f'Меняю цвет на {colour}'

def convert_audio(file_ogg: str) -> str:
    try:
        os.remove(f'voices/{file_ogg}.flac')
    except:
        pass

    name_flac = f'voices/{file_ogg}.flac'
    name_ogg = f'voices/{file_ogg}.ogg'

    process = sp.run(['ffmpeg.exe', '-i', name_ogg, name_flac])
    if process.returncode != 0:
        raise Exception("Что-то пошло не так")

    return name_flac


def execute(bot, res, result):
    try:
        if fuzz.ratio(result, 'зажги свет') >= 80:
            bot.send_message(res.from_user.id, light_on())

        elif fuzz.ratio(result, 'погаси свет') >= 80:
            bot.send_message(res.from_user.id, light_off())
            
        elif fuzz.ratio(result, 'лампочка') >= 75:
            light = device.status()['dps']['20']
            if light:
                bot.send_message(res.from_user.id, light_off())
            else:
                bot.send_message(res.from_user.id, light_on())

        elif fuzz.ratio(result[:12], 'поменяй цвет') >= 80:
            bot.send_message(res.from_user.id, set_color(result[16:]))

        else:
            bot.send_message(res.from_user.id, 'Неизвестная команда!')
    except:
        print('Попробуйте еще раз')