all_cards = [[n, a, b] for n, a, b in zip(range(1, 33), 
                [6, 3,  7,  2, 5, 1, 3, 5, 6, 5, 6, 3,  7, 3, 1, 3, 2, 4, 3, 6, 4, 2, 7, 6, 2,  7, 7, 4, 3,  2, 1, 1],
                [6, 7, 11, 10, 2, 1, 2, 3, 4, 5, 6, 7, 11, 9, 8, 9, 1, 2, 3, 4, 3, 4, 5, 6, 7, 11, 5, 8, 9, 10, 1, 8])]


# dame = [own color, [attributes], [other colors(1=red,2=green,3=purple,4=yellow,5=blue,6=pink)]]
# 1 = heart, 2 = feather, 3 = ring, 4 = chain, 5 = toy, 6 = note, 7 = crown
dames = [ [4, [1, 7, 4], [2, "0 или 2", 1, 1, 1, "0 или 2"], "Люси Морган"], [5, [4, 5, 6], ["0 или 2", 2, "0 или 2", 1, 1, 1], "Энн Хатауэй"],
         [3, [4, 2, 5], ["0 или 2", 1, 1, 1, "0 или 2", 2], "Уинифред Бёрбедж"], [6, [2, 5, 3], [1, "0 или 2", 2, "0 или 2", 1, 1], "Жаклин Филд"],
         [5, [3, 1, 6], ["0 или 2", 2, "0 или 2", 1, 1, 1], "Джейн Давенант"], [2, [6, 3, 5], [1, 1, 1, "0 или 2", 2, "0 или 2"], "Эмилия Ланье"],
         [4, [5, 3, 7], [2, "0 или 2", 1, 1, 1, "0 или 2"], "Пенелопа Рич"], [1, [3, 7, 1], [1, 1, "0 или 2", 2, "0 или 2", 1], "Элизабет Вернон"],
         [6, [1, 4, 2], [1, "0 или 2", 2, "0 или 2", 1, 1], "Мари Маунтджой"], [2, [4, 1, 6], [1, 1, 1, "0 или 2", 2, "0 или 2"], "Энн Уэйтли"],
         [5, [1, 2, 3], ["0 или 2", 1, 1, 1, "0 или 2", 2], "Элин Флорио"],  [1, [7, 4, 5], [1, 1, "0 или 2", 2, "0 или 2", 1], "Мэри Фиттон"]]

list_difficulties = ["Очень легкий", "Легкий", "Средний", "Тяжелый"]
key_difficulties = {"Очень легкий":0, "Легкий":1, "Средний":2, "Тяжелый":3}

list_same = ["Нет, не сможет (игра будет легче)", "Да, сможет (игра будет сложнее)"]

all_diff = [
 [[[10, 11, 27, 9, 21, 20, 23, 24, 13, 25, 32, 29, 17, 16, 26, 4, 3, 2, 1, 12, 28, 14, 6, 7, 19, 18, 30, 5, 8, 22]],  #1lvl notsame 1
  [[14, 13, 26, 2, 11, 10, 24, 23, 20, 21, 9, 8, 22, 27, 1, 25, 12, 32, 15, 29, 4, 3, 16, 6, 7, 19, 5, 17, 18, 30]]], #1lvl same 1

[[[18, 8, 22, 23, 9, 10, 11, 25, 24, 2, 3, 29, 15, 14, 30, 7, 21, 20, 27, 1, 13, 12, 28, 16, 26, 4, 5, 31], #2lvl notsame 1
  [14, 31, 5, 19, 9, 27, 11, 23, 24, 25, 28, 12, 26, 4, 13, 16, 3, 29, 15, 2, 1, 10, 20, 21, 7, 6, 18, 17], #2lvl notsame 2
  [9, 10, 1, 13, 14, 17, 18, 4, 3, 12, 11, 23, 24, 2, 15, 16, 28, 29, 32, 25, 26, 30, 7, 21, 22, 8, 20, 19]], #2lvl notsame 3
 [[15, 16, 31, 17, 7, 19, 21, 22, 27, 24, 12, 13, 1, 2, 28, 29, 3, 4, 30, 5, 8, 18, 6, 14, 26, 11, 25, 32], #2lvl same 1
  [23, 22, 8, 7, 4, 18, 31, 5, 6, 16, 26, 13, 3, 25, 11, 10, 20, 9, 27, 1, 2, 32, 29, 30, 14, 28, 12, 24], #2lvl same 2
  [20, 10, 11, 13, 25, 3, 4, 26, 29, 30, 18, 31, 5, 21, 7, 6, 16, 17, 14, 15, 12, 32, 2, 24, 23, 22, 9, 8]]], #2lvl same 3

[[[7, 30, 16, 31, 18, 6, 5, 17, 29, 28, 14, 26, 25, 15, 2, 24, 13, 11, 12, 3, 1, 10, 20, 21, 9, 19], #3lvl notsame 1
  [17, 29, 3, 4, 26, 14, 31, 16, 30, 5, 21, 20, 10, 1, 25, 28, 12, 24, 23, 22, 8, 9, 19, 7, 6, 18], #3lvl notsame 2
  [32, 2, 13, 30, 29, 28, 12, 24, 10, 22, 8, 5, 19, 7, 21, 18, 17, 14, 15, 25, 3, 1, 23, 11, 26, 16]], #3lvl notsame 3
 [[7, 17, 29, 6, 5, 4, 26, 16, 13, 1, 3, 2, 32, 25, 11, 24, 12, 28, 15, 14, 30, 18, 21, 9, 22, 8], #3lvl same 1
  [2, 32, 28, 12, 24, 3, 30, 29, 16, 26, 25, 15, 14, 31, 5, 21, 9, 8, 18, 19, 7, 4, 13, 1, 10, 11], #3lvl same 2
  [10, 20, 22, 19, 7, 6, 18, 30, 14, 13, 11, 12, 32, 25, 3, 4, 16, 29, 17, 5, 8, 9, 27, 1, 23, 24]]], #3lvl same 3

[[[21, 5, 4, 29, 13, 1, 3, 24, 10, 9, 27, 20, 19, 22, 23, 11, 2, 26, 30, 14, 17, 7, 31, 18],  #4lvl notsame 1
  [7, 4, 16, 17, 14, 32, 25, 28, 12, 15, 29, 30, 18, 19, 20, 23, 1, 10, 22, 27, 9, 21, 5, 8],  #4lvl notsame 2
  [29, 32, 2, 24, 13, 1, 27, 20, 19, 18, 31, 14, 30, 3, 11, 26, 25, 28, 16, 6, 7, 21, 5, 17]], #4lvl notsame 3
 [[4, 16, 6, 7, 21, 9, 8, 19, 20, 10, 22, 23, 24, 27, 11, 13, 1, 12, 2, 26, 14, 30, 3, 29], #4lvl same 1
  [29, 17, 16, 30, 14, 6, 7, 4, 26, 2, 32, 25, 12, 3, 24, 11, 10, 9, 20, 23, 22, 27, 1, 13], #4lvl same 2
  [24, 3, 14, 31, 18, 19, 5, 21, 8, 7, 30, 16, 4, 13, 1, 23, 20, 22, 10, 11, 26, 25, 28, 12]]]] #4lvl same 3

# 1 = Tree, 2 = Cross, 3 = House, 4 = Mask, 5 = Boat, 6 = Beer, 7 = Money, 8 = Fog
city_icons = [[1, 2], [3, 4, 5], [4, 3, 5], [2, 6], [5, 7], [6], [3,2], [4, 1], [3], [2], [7]]

# 1 = Кларкенуэлл, 2 = Блэкфрайерс, 3 = Либерти Клинк, 4 = Саутуарк, 5 = Лондонский мост,
# 6 = Истчип, 7 = Бишопсгейт, 8 = Шордич, 9 = Криплгейт, 10 = Собор Св. Павла, 11 = Корнхилл
city_paths = [[2, 9], [1, 3, 10], [2, 4], [3, 5], [4, 6], [5, 7, 11], [6, 8, 11], [7, 9], [1, 8, 10, 11], [2, 9, 11], [6, 7, 9, 10]]

key_icons = {1:"Предместье", 2:"Церковь", 3:"Дом Шекспира", 4:"Театр", 5:"Набережная", 6:"Трактир", 7:"Место торговли", 8:"Туман"}
key_city = {1:"Кларкенуэлл", 2:"Блэкфрайерс", 3:"Либерти Клинк", 4:"Саутуарк", 5:"Лондонский мост",
            6:"Истчип", 7:"Бишопсгейт", 8:"Шордич", 9:"Криплгейт", 10:"Собор Св. Павла", 11:"Корнхилл"}
key_colors = {1:"Красный", 2:"Зеленый", 3:"Фиолетовый", 4:"Желтый", 5:"Синий", 6:"Розовый"}
key_traits = {1:"Влюбчивая", 2:"Литературно одарённая", 3:"Замужем", 4:"Была связана с Шекспиром", 5:"Есть дети", 6:"Музыкально одарённая", 7:"Есть связи при дворе"}
set_traits = {"Влюбчивая","Литературно одарённая","Замужем","Была связана с Шекспиром","Есть дети","Музыкально одарённая","Есть связи при дворе"}

about_1 = ("Цель игры: Игрок должен разгадать местонахождение  и личность загадочной Смуглой дамы.\n"
"Подготовка к игре: Перед началом игры игроку будет предложено выбрать уровень сложности, их всего 4 (Очень легкий, Легкий, Средний, Тяжелый). Внутри каждого уровня есть также ещё один выбор по сложности - 1. Дама не может оставаться в одной и той же локации (это облегчает игру), 2. Дама может оставаться на одной локации (это чуть сложнее). Таким образом, всего получается 8 уровней сложности. Для ознакомления с игрой рекомендуется использовать уровень сложности - Очень лёгкий (1).\n\n" 
"Начало игры: Игра начинается с карты города Лондона - это игровое поле. На игровом поле 11 локаций с 7 символами ориентиров (обозначения символов можно увидеть в легенде). Темным бордовом цветом обозначается ваше нынешнее положение на карте.\n\n")

about_2 = ("Ход игры: Игрок перемещает своего разведчика по карте города, собирая улики и информацию. Каждый ход игроку дается подсказка о местонахождении дамы в виде символов ориентира, что означает, что дама находится в одном из таких мест. Когда вы делаете свой ход, дама также перемещается в соседнюю локацию. Беглянка никогда не перемещается между городами, не соединёнными линией. Какие есть варианты ваших ходов:\n"
"1. Перемещение на соседнюю локацию\n"
"2. Ждать, т.е остаться на той же локации (дама, в свою очередь, всё равно переместится куда посщитает нужным)\n"
"3.Искать. Если вы считаете, что находитесь с дамой на одной локации, то вы можете попробовать найти ее там. Если это действительно так, то вам будут даны подсказки по ее личности в разделе 'Найденные дамы'.\n\n")

about_3 = ("Разгадывание загадки: Игрок должен анализировать собранные улики и делать предположения о том, где может находиться Чёрная Леди. Он делает свой окончательный ход (разгадка личности), когда считает, что знает её личность и местонахождение. Как разгадать личность и победить?\n"
"- После того, как вы найдете хотя бы одну даму, в кнопке 'Найденные дамы' будут даны подсказки по разгадке ее личности. Например: факт 1, факт 2, факт 3 - общих черт с дамой 2. Это означает, что из трех таких фактов верными являются только 2.\n"
"- Для того, чтобы разгадать личность Смуглой дамы, обычно требуется около трех таких подсказок. На их основе надо будет делать выводы, сопоставлять факты и личности найденных дам.\n"
"- Для разгадки нужно ввести 3 факта о Смуглой даме. В успешном случае вы выиграете.\n\n"
"Конец игры: Если игрок правильно угадал и раскрыл Чёрную Леди, он выигрывает. В противном случае, если он сделал три неправильных предположения о ее личности, он проигрывает.\n\n")

about_4 = ("Примечание:\n"
"- Если в процессе игры вы поймете, что встали в тупик или просто хотите начать новую игру, то введите команду /start с клавиатуры.\n"
"- Игра сложная и требует внимания, так что вовремя прохождения советуем включить мозг и логику\n"
"- Если бот не отвечает сразу, то не надо сто раз тыкать на кнопки. Бот просто думает и даст ответ в течение ближайших секунд")