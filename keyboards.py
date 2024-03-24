import aiogram
from aiogram import types
from aiogram.types import Message

kb_start = [
    [
        types.KeyboardButton(text="Новая игра"),
        types.KeyboardButton(text="О 'Черной Сонате'")
    ],
]
keyboard_start = types.ReplyKeyboardMarkup(keyboard=kb_start, resize_keyboard=True, input_field_placeholder="Добро пожаловать в игру")

kb_about = [
    [
        types.KeyboardButton(text="Новая игра")
    ],
]
keyboard_about = types.ReplyKeyboardMarkup(keyboard=kb_about, resize_keyboard=True, input_field_placeholder="Чтобы начать игру нажми копку")

kb_difficulty = [
    [
        types.KeyboardButton(text="Очень легкий", сallback_data="diff_0"),
        types.KeyboardButton(text="Легкий", сallback_data="diff_1"),
        types.KeyboardButton(text="Средний", сallback_data="diff_2"),
        types.KeyboardButton(text="Тяжелый", сallback_data="diff_3")
    ],
]
keyboard_difficulty = types.ReplyKeyboardMarkup(keyboard=kb_difficulty, resize_keyboard=True, input_field_placeholder="Выбери уровень сложности")

kb_same = [
    [
        types.KeyboardButton(text="Нет, не сможет (игра будет легче)"),
        types.KeyboardButton(text="Да, сможет (игра будет сложнее)"),
    ],
]
keyboard_same = types.ReplyKeyboardMarkup(keyboard=kb_same, resize_keyboard=True, input_field_placeholder="Заканчиваем настройку...")

kb_togame = [
    [
        types.KeyboardButton(text="К игре!"),
    ],
]
keyboard_togame = types.ReplyKeyboardMarkup(keyboard=kb_togame, resize_keyboard=True, input_field_placeholder="Отправляемся на поиски!")

kb_main = [
        [
            types.KeyboardButton(text="Идти"),
            types.KeyboardButton(text="Ждать"),
            types.KeyboardButton(text="Искать"),
            types.KeyboardButton(text="Найденные Дамы")
      ],
    ]
keyboard_main = types.ReplyKeyboardMarkup(keyboard=kb_main, resize_keyboard=True, input_field_placeholder="Ваш ход")

kb_guess = [
    [
        types.KeyboardButton(text="Да, угадываем (конец игры)"),
        types.KeyboardButton(text="Нет, я хочу продолжить играть"),
        types.KeyboardButton(text="Найденные Дамы")
    ],
]
keyboard_guess = types.ReplyKeyboardMarkup(keyboard=kb_guess, resize_keyboard=True, input_field_placeholder="Будем угадывать?")

kb_guess_finish = [
    [
        types.KeyboardButton(text="Влюбчивая"),
        types.KeyboardButton(text="Замужем"),
        types.KeyboardButton(text="Есть дети")
    ],
    [
        types.KeyboardButton(text="Литературно одарённая"),
        types.KeyboardButton(text="Была связана с Шекспиром")
    ],
    [
        types.KeyboardButton(text="Музыкально одарённая"),
        types.KeyboardButton(text="Есть связи при дворе")
    ],
]
keyboard_guess_finish = types.ReplyKeyboardMarkup(keyboard=kb_guess_finish, resize_keyboard=True, input_field_placeholder="Будем угадывать?")

kb_guess_strict = [
    [
        types.KeyboardButton(text="Да, угадываем (конец игры)"),
        types.KeyboardButton(text="Найденные Дамы")
    ],
]
keyboard_guess_strict = types.ReplyKeyboardMarkup(keyboard=kb_guess_strict, resize_keyboard=True, input_field_placeholder="Будем угадывать?")