# на память себе, как удалять кнопки из чата: reply_markup=types.ReplyKeyboardRemove()
# на память как взять юзера из сообщения: user = people[message.from_user.id]
import random
import asyncio
import logging
import sys
from os import getenv
import config
import keyboards
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import *
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import *
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import SendPhoto

# тут будем хранить всех кто пользуется чатом
people = {}

# так выглядят все данные пользователя
class UserInstance:
    def __init__(self, user_id):
        self.user_id = user_id
        self.deck=[]
        self.player_dames = []
        self.player_tile = random.randint(1,11)
        self.dames = config.dames
        self.main_dame = self.dames.pop(random.randrange(len(self.dames)))
        self.main_dame_traits = [config.key_traits.get(self.main_dame[1][0]), config.key_traits.get(self.main_dame[1][1]), config.key_traits.get(self.main_dame[1][2])]
        self.cards_left = 999 
        self.current_card = 0
        self.deck_loops = 2
        self.turn = 0
        self.search_left = 12
        self.game_stop = 0
        self.player_tile_icons = ""
        self.dame_location = ""
        self.dame_icon = ""
        self.dame_run = 0
        self.cards_left_old = ""
        self.main_menu_text = ""
        self.diff_text = ""
        self.same_num = ""
        self.dames_text = "У вас пока нет найденных дам"
        self.dames_guess = []

# создаем разные "этапы" игры. чтобы на одном этапе можно было нажать только то, что разрешено
class game(StatesGroup):
    start =  State() #тут можно либо НОВАЯ ИГРА, либо ОБ ИГРЕ
    difficulty = State() # только выбор сложности
    same = State()  # только выбор same
    togame = State() # только чтобы нажать К ИГРЕ!
    menu = State() # только ИДТИ ЖДАТЬ ИСКАТЬ и ДАМЫ
    dames = State() # мб не нужен
    move = State() # только те варианты КУДА МОЖНО
    guess = State()  # ДАМЫ, ДА угадываем, НЕТ не угадываем
    guess_strict = State() # нельзя отказаться от угадывания
    guess_choose_finish = State()  # только угадывание аргументов и ДАМЫ 
    finish = State() # только команда СТАРТ

# (здесь и ниже цифра 2 в названии только потому что это 2 версия функций)
# динамическое создание клавиатуры, когда нужно дать выбор направления движения
def make_moves_keyboard2(city_paths, message_user_id, key_city):
    global people
    user = people[message_user_id]
    builder = ReplyKeyboardBuilder()
    for city in city_paths[user.player_tile - 1]:
        builder.add(types.KeyboardButton(text=key_city[city]))
    builder.adjust(4)
    return builder

# костыльная функция чтобы вытаскивать из словаря ключ по значению, а не наоборот
def find_key_by_value(dictionary, search_value):
    for key, value in dictionary.items():
        if value == search_value:
            return key
    return None  

# функция записи в файл сообщений пользователя
def write_to_file(message):
    with open("logs.txt", "a") as file:
        file.write(f"{message.from_user.full_name} (@{message.from_user.username}): {message.text}\n")

# функция создания игральной колоды для нынешней сессии игры
def deck_ini2(message_user_id):
    global people
    user = people[message_user_id]
    difficulty = config.key_difficulties[user.diff_text]
    user.deck = [config.all_cards[i-1] for i in config.all_diff[difficulty][user.same_num][random.randrange(len(config.all_diff[difficulty][user.same_num]))]]
    rand_shuffle = random.randrange(len(user.deck))
    user.deck = user.deck[rand_shuffle:] + user.deck[:rand_shuffle]

#функция обновления хода ("ход компьютера")
def update_turn2(message_user_id): # message_user_id = message.from_user.id
    global people
    user = people[message_user_id]
    user.turn = user.turn+1
    if user.dame_run == 1:
        user.current_card = (user.deck.index(user.deck[user.current_card]) +1 + len(user.player_dames)) % len(user.deck)
        user.dame_run = 0
    else:
        user.current_card = (user.deck.index(user.deck[user.current_card]) + 1) % len(user.deck)
    user.cards_left_old=user.cards_left
    user.cards_left=len(user.deck)-user.current_card
    if user.cards_left >user.cards_left_old:
        user.deck_loops=user.deck_loops-1
        if user.deck_loops < 0:
            user.game_stop = 1
    user.dame_location = user.deck[user.current_card][2]
    user.dame_icon = user.deck[user.current_card][1]
    user.player_tile_icons = ", ".join(config.key_icons[value] for value in config.city_icons[user.player_tile - 1])
    user.main_menu_text = (f"<b>{user.turn}</b> ход\n"
                  f"Дама - там, где есть {config.key_icons.get(user.dame_icon)}\n"
                  f"В колоде осталось <b>{user.cards_left}</b> карт\n"
                  f"Осталось колод помимо этой: <b>{user.deck_loops}</b>\n\n"
                  f"Статус:\nТы находишься в {config.key_city.get(user.player_tile)}.\n"
                  f"В твоей локации есть: {user.player_tile_icons}\n"
                  f"Осталось попыток найти Даму: {user.search_left}")
    if len(user.player_dames) == 0:
        user.dames_text = "У вас пока нет найденных дам"
    else:
        user.dames_text = ""
        for dame in user.player_dames:
            user.dames_text += f"<b>{dame[3]}</b>\n"
            user.dames_text += f"<i>- {config.key_traits.get(dame[1][0])}\n- {config.key_traits.get(dame[1][1])}\n- {config.key_traits.get(dame[1][2])}</i>\n"
            user.dames_text += f"Общий черт с вашей Дамой: <b>{dame[2][user.main_dame[0]-1]}</b>\n\n"

# функция создающая нужные данные для игры. запускается только 1 раз, в нулевой ход
def ini_turn2(message_user_id):
    global people
    user = people[message_user_id]
    user.cards_left=len(user.deck)
    user.dame_location = user.deck[user.current_card][2]
    user.dame_icon = user.deck[user.current_card][1]
    user.player_tile_icons = ", ".join(config.key_icons[value] for value in config.city_icons[user.player_tile - 1])
    player_status_dame_icon = ""
    if user.dame_icon == 8:
        player_status_dame_icon = "Дама в тумане"
    else:
        player_status_dame_icon = f"Дама - там, где есть {config.key_icons.get(user.dame_icon)}"
    user.main_menu_text = (f"<b>{user.turn}</b> ход\n"
                  f"{player_status_dame_icon}\n"
                  f"В колоде осталось <b>{user.cards_left}</b> карт\n"
                  f"Осталось колод помимо этой: <b>{user.deck_loops}</b>\n\n"
                  f"Статус:\nТы находишься в {config.key_city.get(user.player_tile)}.\n"
                  f"В твоей локации есть: {user.player_tile_icons}\n"
                  f"Осталось попыток найти Даму: {user.search_left}")

# функция вытаскивания фотографии для локации, в которой игрок сейчас 
def image_choose2(message_user_id):
    global people
    user = people[message_user_id]
    image = FSInputFile(f"photos/{user.player_tile}.jpg")
    return image

# токен бота
TOKEN = "6917901953:AAFXpSIzNxhe4uQHxW8nwK6--a3PWlBn5A8"

# создание диспетчера, принимающего сообщения.
# его легко представить как "сито" - если не удовлетворено условие верхнего хэндлера (обработчика),
# то проверяется следующий 
dp = Dispatcher()

# ловит команду /start. Всегда. Создает пользователя, если его нет
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user_id = message.from_user.id
    if user_id not in people:
        people[user_id] = UserInstance(user_id)
    await message.answer(f"Привет, {hbold(message.from_user.first_name)}!\n"
                     "Этот бот - адаптация настольной игры 'Черная Соната'\n"
                     "\nДля взаимодействия с ботом используй кнопки внизу экрана", reply_markup=keyboards.keyboard_start)
    await state.set_state(game.start)
    
# отлавливает все иные сообщения, которые отправляют после перезапуска бота. выдает команду /start, чтобы ее не вводить руками
@dp.message(StateFilter(None))
async def command_start_handler(message: Message):
    write_to_file(message)
    await message.answer(f"Кажется, бот был перезапущен...\n\n"
                     "/start - чтобы разбудить бота")

# описание игры, правила
@dp.message(game.start, F.text == "О 'Черной Сонате'")
async def command_about_handler(message: Message, state: FSMContext):
    write_to_file(message)
    image = FSInputFile("photos/Base_map_BS.jpg")
    await message.answer_photo(image, "<b>Черная Соната 1/4</b>\n\n"
                                      f"{config.about_1}",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=keyboards.keyboard_about)
    await message.answer("<b>Черная Соната 2/4</b>\n\n"
                                      f"{config.about_2}",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=keyboards.keyboard_about)
    await message.answer("<b>Черная Соната 3/4</b>\n\n"
                                      f"{config.about_3}",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=keyboards.keyboard_about)
    await message.answer("<b>Черная Соната 4/4</b>\n\n"
                                      f"{config.about_4}",
                                      parse_mode=ParseMode.HTML,
                                      reply_markup=keyboards.keyboard_about)

# переход к игре. просит выбрать уровень сложности
@dp.message(game.start, F.text == "Новая игра")
async def command_newgame_handler(message: Message, state: FSMContext):
    write_to_file(message)
    await message.answer("Выбери уровень сложности:",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_difficulty)
    await state.set_state(game.difficulty)

# здесь и ниже: последний хендлер с конкретным статусом (тут - "game.start") и без аргументов нужен, чтобы ловить все неправильные сообщения
@dp.message(game.start)
async def command_about_handler(message: Message):
    write_to_file(message)
    await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_start)

# ловит сообщения, если введена правильная сложность. 
# обрабатывает сложность и предлает выбрать, можно ли Даме быть в одной и той же локации больше 1 хода подряд
@dp.message(game.difficulty, F.text.in_(config.list_difficulties))
async def set_diff_ok(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    user.diff_text = message.text
    await message.answer(f"Уровень сложности <b>{message.text}</b>\n\n"
                        "Сможет ли Дама оставаться в одной локации больше 1 хода подряд?",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_same)
    await state.set_state(game.same)

# ловит неправильный ввод при выборе сложности (аналогично хендлеру выше)
# ниже буду просто писать "ловит неправильный ввод" для таких же случаев
@dp.message(game.difficulty)
async def set_diff_error(message: Message):
    write_to_file(message)
    await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_difficulty)

# если настройка перемещений Дамы правильная, предлагает переходить к игре
@dp.message(game.same, F.text.in_(config.list_same))
async def set_same_ok(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    if message.text == config.list_same[0]:
        user.same_num = 0
        await message.answer(f"Дама каждый ход будет в <b>новой</b> локации\n\n"
                          "Ура, настройка завершена! Можно переходить к игре",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_togame)
        await state.set_state(game.togame)
    elif message.text == config.list_same[1]:
        user.same_num = 1
        await message.answer(f"Дама <b>сможет</b> находиться в одной локации несколько ходов подряд\n\n"
                          "Ура, настройка завершена! Можно переходить к игре",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_togame)
        await state.set_state(game.togame)

# ловит неправильный ввод
@dp.message(game.same)
async def set_same_error(message: Message):
    write_to_file(message)
    await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_same)

# начинает игру, создает колоду и обновляет пользовательские данные (расположение на поле, кол-во ходов и тп)
@dp.message(game.togame, F.text == "К игре!")
async def window_main_0(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    deck_ini2(message.from_user.id)
    ini_turn2(message.from_user.id)
    await message.answer_photo(image_choose2(message.from_user.id),f"{user.main_menu_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_main)
    await state.set_state(game.menu)

# ловит неправильный ввод
@dp.message(game.togame)
async def window_main_0_error(message: Message):
    write_to_file(message)
    await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_togame)

# обрабатывает 1 из 3 вариантов хода - ждать. Самый простой. Только обновляет переменные
@dp.message(game.menu, F.text == "Ждать")
async def window_wait(message: Message):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    update_turn2(message.from_user.id)
    if user.deck_loops == -1:
        await message.answer(f"К сожалению, у тебя кончились карты в колоде\n\n"
                                     f"Это конец игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
        await message.answer(f"/start для новой игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(game.finish)
    else:
        await message.answer_photo(image_choose2(message.from_user.id),f"Подождали\n\n"
                         f"{user.main_menu_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_main)

# не является игровым "ходом", красиво выводит на экран всех Дам, которые есть у игрока.
# Ниже будут аналогичные хэндлеры, разница в статусе игры (тут - game.menu)
@dp.message(game.menu, F.text == "Найденные Дамы")
async def window_search_dames(message: Message):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    await message.answer(f"Найденные Дамы:\n\n"
                        f"{user.dames_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_main)

# обрабатывает 1 из 3 вариантов хода - идти. 
# переводит игрока в статус выбора направления передвижения game.move
@dp.message(game.menu, F.text == "Идти")
async def window_move(message: Message, state: FSMContext):
    write_to_file(message)
    builder = make_moves_keyboard2(config.city_paths, message.from_user.id, config.key_city)
    await message.answer(f"Куда идем?\n",
                         parse_mode=ParseMode.HTML,
                         reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(game.move)

# обрабатывает 1 из 3 вариантов хода - искать. 
# самый комплексный вариант хода, необходимо проверять много условий. 
# Если Дама найдена, предлагает игроку угадать черты своей (основной) Дамы.
# При вопросе переводит игрока в статус game.guess или .guess_strict, если это последний шанс угадать Даму
@dp.message(game.menu, F.text == "Искать")
async def window_search(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    if user.deck[user.current_card][1] == 8:
       await message.answer_photo(image_choose2(message.from_user.id),f"Нельзя искать Даму когда она в тумане\n\n"
                         f"{user.main_menu_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_main) 
    else:
        user.search_left = user.search_left - 1
        user.deck[user.current_card][1] = 8
        if user.dame_location != user.player_tile:
            user.dame_run = 1
            update_turn2(message.from_user.id)
            if user.deck_loops == -1:
                await message.answer(f"К сожалению, у тебя кончились карты в колоде\n\n"
                                     f"Это конец игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
                await message.answer(f"/start для новой игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
                await state.set_state(game.finish)
            else:
                await message.answer_photo(image_choose2(message.from_user.id),f"Дамы здесь нет\n\n"
                         f"Ваши поиски напугали Даму и помимо своего хода она убежала еще на +{len(user.player_dames)+1} ходов вперед\n\n"
                         f"{user.main_menu_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_main)
                if user.search_left == 0:
                    await message.answer(f"К сожалению, у тебя кончились попытки угадать, где Дама\n\n"
                                     f"Это конец игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
                    await message.answer(f"/start для новой игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
                    await state.set_state(game.finish)
        elif user.dame_location == user.player_tile:
            user.dame_run = 1
            user.player_dames.append(user.dames.pop(random.randrange(len(user.dames))))
            update_turn2(message.from_user.id)
            if user.search_left == 0 or user.deck_loops == -1:
                await state.set_state(game.guess_strict)
                await message.answer(f"Дама здесь!\n\n"
                         f"Хотите попробовать угадать ее черты?\n"
                         "Попытка угадать только <b>одна</b>!\n\n"
                         "У вас больше нет попыток ее найти (или кончились карты в колоде), поэтому отказаться нельзя!",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess_strict)
            else:
                await state.set_state(game.guess)
                await message.answer(f"Дама здесь!\n\n"
                         f"Хотите попробовать угадать ее черты?\n"
                         "Попытка угадать только <b>одна</b>!",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess)

# ловит неправильный ввод
@dp.message(game.menu)
async def window_menu_error(message: Message):
    write_to_file(message)
    await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_main)

# обрабатывает варинты передвижения игрока. 
# также ловит неправильный ввод, тк клавиатура для перемещения динамическая и сделать проверку на ввод внутри хэнлера было проще
@dp.message(game.move)
async def window_move(message: Message, state: FSMContext):
    write_to_file(message)
    global player_tile
    global people
    user = people[message.from_user.id]
    if find_key_by_value(config.key_city, message.text) in config.city_paths[user.player_tile-1]:
        user.player_tile = find_key_by_value(config.key_city, message.text)
        update_turn2(message.from_user.id)
        if user.deck_loops == -1:
            await message.answer(f"К сожалению, у тебя кончились карты в колоде\n\n"
                                     f"Это конец игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f"/start для новой игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(game.finish)
        else:
            await message.answer_photo(image_choose2(message.from_user.id),f"Перешли в <b>{message.text}</b>\n\n"
                             f"{user.main_menu_text}",
                             parse_mode=ParseMode.HTML,
                             reply_markup=keyboards.keyboard_main)
            await state.set_state(game.menu)
    else:
        builder = make_moves_keyboard2(config.city_paths, message.from_user.id, config.key_city)
        await message.answer("<b>Ошибка</b>\n\n"
                             "Некорректный запрос на перемещение",
                             parse_mode=ParseMode.HTML,
                             reply_markup=builder.as_markup(resize_keyboard=True))

# обрабатывает отказ от угадывания черт Дамы
# переносит игрока обратно в меню
@dp.message(game.guess, F.text == "Нет, я хочу продолжить играть")
async def window_search_abort(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    await message.answer_photo(image_choose2(message.from_user.id),f"Хорошо, продолжаем играть\n"
                         f"Ваши поиски напугали Даму и помимо своего хода она убежала еще на +{len(user.player_dames)+1} ходов вперед\n\n"
                         f"{user.main_menu_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_main)
    await state.set_state(game.menu)

# переводит игрока на угаывание черт, если он согласился 
@dp.message(game.guess, F.text == "Да, угадываем (конец игры)")
async def window_search_choose(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    await message.answer(f"Выбери 3 черты дамы\n\n"
                        "Нажимать можно в любом порядке",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess_finish)
    await state.set_state(game.guess_choose_finish)

# не является ходом, но позволяет посмотреть найденных дам прежде чем принимать решение, угадывать черты своей или нет. 
@dp.message(game.guess, F.text == "Найденные Дамы")
async def window_search_dames(message: Message):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    await message.answer(f"Найденные Дамы:\n\n"
                        f"{user.dames_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess)

# ловит неправильный ввод
@dp.message(game.guess)
async def window_search_error(message: Message):
    write_to_file(message)
    await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess)

# аналогично хэндлеру выше, принимает согласие от игрока, 
# но этот - в случае, если игрок в статусе game.guess_strict и ему НУЖНО угадывать сейчас иначе он проиграет
@dp.message(game.guess_strict, F.text == "Да, угадываем (конец игры)")
async def window_search_choose(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    await message.answer(f"Выбери 3 черты дамы\n\n"
                        "Нажимать можно в любом порядке",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess_finish)
    await state.set_state(game.guess_choose_finish)

# аналогично хэнлеру выше, позволяет просмотреть найденных дам, но в статусе game.guess_strict
@dp.message(game.guess_strict, F.text == "Найденные Дамы")
async def window_search_dames(message: Message):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    await message.answer(f"Найденные Дамы:\n\n"
                        f"{user.dames_text}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess)
    
# ловит неправильный ввод
@dp.message(game.guess_strict)
async def window_search_error(message: Message):
    write_to_file(message)
    await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess)

# ловит все сообщения при угадывании черт Дамы. 
# например, для победы необходимо угадать все 3 черты, 
# поэтому, при отгадывании черт, сообщения игрока попадут в этот хендлер
#минимум 3 раза - по 1 на каждую черту
@dp.message(game.guess_choose_finish)
async def window_search_error(message: Message, state: FSMContext):
    write_to_file(message)
    global people
    user = people[message.from_user.id]
    if message.text in user.main_dame_traits:
        if message.text not in user.dames_guess:
            user.dames_guess.append(message.text)
            if len(user.dames_guess) < 3:
                await message.answer(f"Отлично, {message.text} - действительно про нее\n\n"
                                     f"Осталось угадать {3-len(user.dames_guess)}",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=keyboards.keyboard_guess_finish)
            else:
                await message.answer(f"Отлично, {message.text} - действительно про нее\n\n"
                                     f"Ура! Вы нашли Смуглую даму и преуспели в деле, с которым литературоведы"
                                     f"и историки не могли справиться в течение четырёх веков",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
                await message.answer(f"/start для новой игры",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=types.ReplyKeyboardRemove())
                await state.set_state(game.finish)
        else:
            await message.answer(f"Да-да, ты уже это тыкал\n\n"
                                 f"Осталось угадать {3-len(user.dames_guess)}",
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=keyboards.keyboard_guess_finish)
    else:
        if message.text not in config.set_traits:
            if message.text == "Найденные Дамы":
                await message.answer(f"Найденные Дамы:\n\n"
                                     f"{user.dames_text}",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=keyboards.keyboard_guess_finish)
            else:
                await message.answer("<b>Ошибка</b>\n\n"
                         "Некорректный запрос",
                         parse_mode=ParseMode.HTML,
                         reply_markup=keyboards.keyboard_guess_finish)
        else:
            traits_output = '\n'.join(user.main_dame_traits)
            await message.answer("К сожалению, этой черты у Дамы нет\n\n"
                         f"Верный ответ был: {traits_output}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=types.ReplyKeyboardRemove())
            traits_output = ""
            await message.answer(f"/start для новой игры",
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(game.finish)

#=========================
# main
async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    with open("logs.txt", "w") as file:
        file.write("logs:\n")
    asyncio.run(main())
    