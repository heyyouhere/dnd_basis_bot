from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler, MessageHandler
from telegram.constants import ParseMode
import basis_api as basis
from basis_api import RaceType, ClassType, SkillType, EventType
import random
import texts as t

CAPSULE_CODE = 'WHJXHRHDG'

IS_ROUND = False

PERSONAL_DATA = '''
Для использования сервиса в соответствии
с Федеральным законом от 27.07.2006 Nº 152-ФЗ «О
персональных даных» требуется получение Вашего
согласия на обработку персональных данных'''

ALLOWED_USER_IDS = [
    1899008325,
    249484136,
]

INTRO_1_MESSAGE = t.intro_message

RACES = [
    'Человек',
    'Арктурианец',
    'Звёздный бродяга',
]

CLASSES = [
    'Разведчик',
    'Хакер',
    'Штурмовик',
]

SKILLS = [
    'Сила',
    'Ловкость',
    'Интеллект',
]


# GAME STATES
INTRO1, CHOOSE_RACE, INTRO2, CHOOSE_CLASS, CAPSULE, HANDLE_CAPSULE, INTRO3, QUESTION_1, HANDLE_QUESTION_1, GET_EMAIL, QUESTION_2, GET_NUMBER, QUESTION_3, QUESTION_4, AR, END, DISTRIBUTE, CODE_CAPSULE, CODE_CAPSULE_QUERY, CODE_AR, HANDLE_AR = range(21)

def find_player_index(user_id, player_list):
    for index, player in enumerate(player_list):
        if player["tg_id"] == user_id:
            return index
    return -1  # Return -1 if the player is not found in the list

def define_stats(player_data, user_id):
    if player_data:
        print(player_data)
        race = player_data['character_race']
        player_class = player_data['character_class']
        top_users = basis.get_top_users(3)
        all_players = basis.get_all_users_tg_id()
        your_place = find_player_index(user_id, all_players)

        race_name = "Неизвестная раса"
        class_name = "Неизвестный класс"
        image_url = './img/placeholder.jpeg'

        ar_points = player_data['ar_points']
        if player_data['activities_finished']['WHEEL']:
            wheel_quest = 'Пройден'
        else:
            wheel_quest = 'Не пройден'
        total_skill_points = player_data['total_skill_points']

        formatted_top_users = f"Место - Имя - Баллы\n"

        caption_text = ''

        for index, user in enumerate(top_users, start=1):
            user_info = f"{index} - {user['username']} - {user['total_skill_points']}"
            formatted_top_users += user_info

            if index != len(top_users):
                formatted_top_users += "\n"

        if race == 1:
            race_name = 'Человек'
            if player_class == 1:
                class_name = 'Штурмовик'
                image_url = './img/HUMAN_TROOPER.png'
            elif player_class == 2:
                image_url = './img/HUMAN_SPY.png'
                class_name = 'Разведчик'
            elif player_class == 3:
                image_url = './img/HUMAN_HACKER.png'
                class_name = 'Хакер'
        elif race == 2:
            race_name = 'Актурианец'
            if player_class == 1:
                class_name = 'Штурмовик'
                image_url = './img/ACTUR_TROOPER.png'
            elif player_class == 2:
                image_url = './img/ACTUR_SPY.png'
                class_name = 'Разведчик'
            elif player_class == 3:
                image_url = './img/ACTUR_HACKER.png'
                class_name = 'Хакер'
        elif race == 3:
            race_name = 'Звёздный бродяга'
            if player_class == 1:
                class_name = 'Штурмовик'
                image_url = './img/HOBO_TROOPER.png'
            elif player_class == 2:
                image_url = './img/HOBO_SPY.png'
                class_name = 'Разведчик'
            elif player_class == 3:
                image_url = './img/HOBO_HACKER.png'
                class_name = 'Хакер'

        caption_text += f'-----------------------\n'
        caption_text = f"Раса: {race_name}\nКласс: {class_name}\nОчки:\n🦾Сила - {player_data['skills']['STR']}\n👩🏼‍🚀Ловкость - {player_data['skills']['AGL']}\n🧠Интеллект - {player_data['skills']['WIS']}\n\nКвесты:\nAR - {ar_points}\nКапсула - {wheel_quest}\n"
        caption_text += f'-----------------------\n'
        caption_text += f'{formatted_top_users}\n'
        caption_text += f'-----------------------\n'
        caption_text += f"{your_place + 1} - {player_data['username']} - {total_skill_points}"

        return (image_url, caption_text)
    else:
        return ('./img/placeholder.jpeg', 'Данные не найдены')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not IS_ROUND:
        await context.bot.send_message(chat_id=update.message.chat_id, text='👾')
        """Соглашение об обработке персональных данных"""
        keyboard = [
            [
                InlineKeyboardButton("Я согласен", callback_data="agree"),
                InlineKeyboardButton("Не согласен", callback_data="disagree"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(PERSONAL_DATA, reply_markup=reply_markup)
        return INTRO1
    else:
        await update.message.reply_text('Сейчас идет финальный раунд на стенде Базис, после его окончания вы сможете принять участие в игре')

async def intro1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """интро 1"""
    query = update.callback_query
    user_id = update.effective_user.id
    username = update.effective_user.username
    chat_id = query.message.chat.id
    await context.bot.send_message(chat_id=chat_id, text='👽')

    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Дальше", callback_data="Дальше"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if query.data == 'agree':
        basis.create_character(user_id, username, chat_id)
        #print('USER HAS BEEN CREATED')
        await update.callback_query.edit_message_reply_markup(None)
        await query.message.reply_text(INTRO_1_MESSAGE, reply_markup=reply_markup)
        return CHOOSE_RACE
    else:
        keyboard = [
        [
            InlineKeyboardButton("Я согласен", callback_data="agree"),
            InlineKeyboardButton("Не согласен", callback_data="disagree"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_reply_markup(None)
        await query.message.reply_text(PERSONAL_DATA, reply_markup=reply_markup)
        return INTRO1

async def choose_race(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выбираем расу"""
    query = update.callback_query

    chat_id = query.message.chat.id
    await context.bot.send_message(chat_id=chat_id, text='🔭')

    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(RACES[0], callback_data=RACES[0]),
            InlineKeyboardButton(RACES[1], callback_data=RACES[1]),
        ],
        [
            InlineKeyboardButton(RACES[2], callback_data=RACES[2]),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_reply_markup(None)
    await query.message.reply_text(t.race_message, reply_markup=reply_markup)
    return CHOOSE_CLASS

async def choose_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбираем класс"""
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()
    chat_id = query.message.chat.id
    await context.bot.send_message(chat_id=chat_id, text='🦾')
    # set character race
    match query.data:
        case 'Человек':
            #print("PACE HAS BEEN CHOOSEN - HUMAN")
            basis.set_race(user_id, basis.RaceType.HUMAN)
        case 'Звёздный бродяга':
            #print("PACE HAS BEEN CHOOSEN - HOBO")
            basis.set_race(user_id, basis.RaceType.HOBO)
        case 'Актурианец':
            #print("PACE HAS BEEN CHOOSEN - ACTUR")
            basis.set_race(user_id, basis.RaceType.ACTUR)

    keyboard = [
        [
            InlineKeyboardButton("Дальше", callback_data="Дальше"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(None)

    await query.message.reply_text(t.after_race_message, reply_markup=reply_markup)
    return INTRO2

    # keyboard = [
    #     [
    #         InlineKeyboardButton(CLASSES[0], callback_data=CLASSES[0]),
    #         InlineKeyboardButton(CLASSES[1], callback_data=CLASSES[1]),
    #     ],
    #     [
    #         InlineKeyboardButton(CLASSES[2], callback_data=CLASSES[2]),
    #     ],
    # ]
    # await query.message.reply_text(t.after_race_message)
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # await update.callback_query.edit_message_reply_markup(None)
    # await query.message.reply_text(t.class_message, reply_markup=reply_markup)

    # return CAPSULE

async def intro2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """интро 2"""

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(CLASSES[0], callback_data=CLASSES[0]),
            InlineKeyboardButton(CLASSES[1], callback_data=CLASSES[1]),
        ],
        [
            InlineKeyboardButton(CLASSES[2], callback_data=CLASSES[2]),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(None)
    await query.message.reply_text(t.class_message, reply_markup=reply_markup)

    return CAPSULE

async def capsule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбираем скилы"""
    query = update.callback_query
    user_id = update.effective_user.id

    await query.answer()
    # set character class
    match query.data:
        case 'Разведчик':
            #print("CLASS HAS BEEN CHOOSEN - SPY")
            basis.set_class(user_id, basis.ClassType.SPY)
        case 'Хакер':
            #print("CLASS HAS BEEN CHOOSEN - HACKER")
            basis.set_class(user_id, basis.ClassType.HACKER)
        case 'Штурмовик':
            #print("CLASS HAS BEEN CHOOSEN - TROOPER")
            basis.set_class(user_id, basis.ClassType.TROOPER)

    keyboard = [
        [
            InlineKeyboardButton('Ввести код', callback_data='enter_capsule_code'),
        ],
        [
            InlineKeyboardButton('Пропустить', callback_data='capsule_skip'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(None)
    await query.message.reply_text(t.capsule_message, reply_markup=reply_markup)

    return HANDLE_CAPSULE

async def handle_capsule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    user_id = update.effective_user.id
    chat_id = query.message.chat.id
    await context.bot.send_message(chat_id=chat_id, text='💡')
    await query.answer()
    # set character class
    match query.data:
        case 'capsule_skip':
            # keyboard = [
            #     [
            #         InlineKeyboardButton('Ответ 1', callback_data='q1_1'),
            #         InlineKeyboardButton('Ответ 2', callback_data='q1_2'),
            #     ],
            #     [
            #         InlineKeyboardButton('Ответ 3', callback_data='q1_3'),
            #     ],
            # ]

            # reply_markup = InlineKeyboardMarkup(keyboard)
            # await update.callback_query.edit_message_reply_markup(None)
            # # await query.message.reply_text(t.before_first_question)
            # await query.message.reply_text('''Вопрос 1''', reply_markup=reply_markup)
            # return QUESTION_1
            keyboard = [
                [
                    InlineKeyboardButton("Дальше", callback_data="Дальше"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_reply_markup(None)

            await query.message.reply_text(t.before_first_question, reply_markup=reply_markup)
            return INTRO3

        case 'enter_capsule_code':
            character_data = basis.get_character_data(user_id)
            activities_finished = character_data['activities_finished']
            if activities_finished['WHEEL']:
                await query.message.reply_text('''Вы уже вводили код от капсулы''')
                return QUESTION_1
            await query.message.reply_text('''Введите код от капсулы: ''')
            return CODE_CAPSULE

async def intro3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """интро 3"""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(t.first_question_answers[0], callback_data='q1_1'),
        ],
        [
            InlineKeyboardButton(t.first_question_answers[1], callback_data='q1_2'),
        ],
        [
            InlineKeyboardButton(t.first_question_answers[2], callback_data='q1_3'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_reply_markup(None)

    await query.message.reply_text(t.first_question, reply_markup=reply_markup)
    return QUESTION_1

async def question1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    match query.data:
        case 'q1_2':
            keyboard = [
                [
                    InlineKeyboardButton('Сила', callback_data='1-GET_EMAIL-skill_STR'),
                    InlineKeyboardButton('Ловкость', callback_data='1-GET_EMAIL-skill_AGL'),
                ],
                [
                    InlineKeyboardButton('Интеллект', callback_data='1-GET_EMAIL-skill_WIS'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text('''Вы ответили верно. Выберите характеристику, которую вы хотите улучшить (+1)''', reply_markup=reply_markup)
            return DISTRIBUTE
        case _:
            await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text('''Ответ неверный\n\n''' + t.get_email_message)
            return GET_EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    #print('GET EMAIL STAGE')
    user_input = update.message.text
    user_id = update.effective_user.id
    # await update.message.reply_text(f'Вы ввели {user_input}')
    await context.bot.send_message(chat_id=update.message.chat_id, text='💡')
    # keyboard = [
    #             [
    #                 InlineKeyboardButton(t.second_question_answers[0], callback_data='q1_1'),
    #             ],
    #             [
    #                 InlineKeyboardButton(t.second_question_answers[1], callback_data='q1_2'),
    #             ],
    #             [
    #                 InlineKeyboardButton(t.second_question_answers[2], callback_data='q1_3'),
    #             ],
    #             [
    #                 InlineKeyboardButton(t.second_question_answers[3], callback_data='q1_3'),
    #             ],
    #             [
    #                 InlineKeyboardButton(t.second_question_answers[4], callback_data='q1_3'),
    #             ],
    #         ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    # await update.message.reply_text(t.second_question, reply_markup=reply_markup)
    # # TODO сохранять имейл
    keyboard = [
                [
                    InlineKeyboardButton('Сила', callback_data='1-QUESTION_2-skill_STR'),
                    InlineKeyboardButton('Ловкость', callback_data='1-QUESTION_2-skill_AGL'),
                ],
                [
                    InlineKeyboardButton('Интеллект', callback_data='1-QUESTION_2-skill_WIS'),
                ],
            ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('''Выбери характеристику, которую ты хочешь улучшить (+1)''', reply_markup=reply_markup)
    basis.set_mail(user_id, user_input)
    return DISTRIBUTE
    # return QUESTION_2

async def question2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    match query.data:
        case 'q1_2':
            keyboard = [
                [
                    InlineKeyboardButton('Сила', callback_data='1-GET_NUMBER-skill_STR'),
                    InlineKeyboardButton('Ловкость', callback_data='1-GET_NUMBER-skill_AGL'),
                ],
                [
                    InlineKeyboardButton('Интеллект', callback_data='1-GET_NUMBER-skill_WIS'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text('''Вы ответили верно. Выберите характеристику, которую вы хотите улучшить (+1)''', reply_markup=reply_markup)
            return DISTRIBUTE
        case _:
            await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text('''Ответ неверный\n\n''' + t.get_number_message)
            return GET_NUMBER

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    #print('GET NUMBER STAGE')
    user_input = update.message.text
    user_id = update.effective_user.id
    # await update.message.reply_text('📱')
    # keyboard = [
    #             [
    #                 InlineKeyboardButton(t.third_question_answers[0], callback_data='q1_1'),
    #                 InlineKeyboardButton(t.third_question_answers[1], callback_data='q1_2'),
    #             ],
    #             [
    #                 InlineKeyboardButton(t.third_question_answers[2], callback_data='q1_3'),
    #             ],
    #         ]

    # reply_markup = InlineKeyboardMarkup(keyboard)
    # # await update.callback_query.edit_message_reply_markup(None)
    # await update.message.reply_text(t.third_question, reply_markup=reply_markup)
    keyboard = [
                [
                    InlineKeyboardButton('Сила', callback_data='1-QUESTION_3-skill_STR'),
                    InlineKeyboardButton('Ловкость', callback_data='1-QUESTION_3-skill_AGL'),
                ],
                [
                    InlineKeyboardButton('Интеллект', callback_data='1-QUESTION_3-skill_WIS'),
                ],
            ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('''Выбери характеристику, которую ты хочешь улучшить (+1)''', reply_markup=reply_markup)
    basis.set_phone(user_id, user_input)
    return DISTRIBUTE
    # return QUESTION_3

async def question3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    match query.data:
        case 'q1_1':
            keyboard = [
                [
                    InlineKeyboardButton('Сила', callback_data='1-QUESTION_4-skill_STR'),
                    InlineKeyboardButton('Ловкость', callback_data='1-QUESTION_4-skill_AGL'),
                ],
                [
                    InlineKeyboardButton('Интеллект', callback_data='1-QUESTION_4-skill_WIS'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text('''Вы ответили верно. Выберите характеристику, которую вы хотите улучшить (+1)''', reply_markup=reply_markup)
            return DISTRIBUTE
        case _ :
            # await update.callback_query.edit_message_reply_markup(None)
            await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text('''Ответ неверный\n\n''')
            await query.message.reply_text(t.forth_question)
            return QUESTION_4

async def question4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text

    await update.message.reply_text(f'Вы ввели {user_input}')

    match user_input:
        case '310' | '3-10' | '3 10' | '3—10':
            keyboard = [
                [
                    InlineKeyboardButton('Сила', callback_data='1-BEFORE_AR-skill_STR'),
                    InlineKeyboardButton('Ловкость', callback_data='1-BEFORE_AR-skill_AGL'),
                ],
                [
                    InlineKeyboardButton('Интеллект', callback_data='1-BEFORE_AR-skill_WIS'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text('''Вы ответили верно. Выберите характеристику, которую вы хотите улучшить (+1)''', reply_markup=reply_markup)
            return DISTRIBUTE
        case _ :
            keyboard = [
                [
                    InlineKeyboardButton('Ввести код', callback_data='enter_ar_code'),
                ],
                [
                    InlineKeyboardButton('Пропустить', callback_data='ar_skip'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            # await update.callback_query.edit_message_reply_markup(None)
            await update.message.reply_text('Неверно (\n' + t.ar_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            return AR

async def ar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = update.effective_user.id

    await query.answer()
    # set character class
    match query.data:
        case 'ar_skip':
            await update.callback_query.edit_message_reply_markup(None)
            user_id = update.effective_user.id
            player_data = basis.get_character_data(user_id)
            image_url, caption_text = define_stats(player_data, user_id)
            keyboard = [
                [
                    InlineKeyboardButton("Дальше", callback_data="Дальше"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if player_data:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=f'{caption_text}', reply_markup=reply_markup)
            else:
                pass
            return END
        case 'enter_ar_code':
            await update.callback_query.edit_message_reply_markup(None)
            character_data = basis.get_character_data(user_id)
            activities_finished = character_data['activities_finished']
            if activities_finished['AR']:
                await query.message.reply_text('''Вы уже вводили код от AR''')
                return END
            await query.message.reply_text('''Введите код от AR: ''')
            return CODE_AR

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await update.callback_query.edit_message_reply_markup(None)
    await query.message.reply_text(t.final_message, parse_mode=ParseMode.MARKDOWN)
    return ConversationHandler.END

async def distribute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    await update.callback_query.edit_message_reply_markup(None)

    points, stage, answer = query.data.split('-')
    match answer:
        case 'skill_STR':
            #print('SKILL STR HAS BEEN UPGRADED')
            basis.update_skill(user_id, basis.SkillType.STR, int(points))
        case 'skill_AGL':
            #print('SKILL AGL HAS BEEN UPGRADED')
            basis.update_skill(user_id, basis.SkillType.AGL, int(points))
        case 'skill_WIS':
            #print('SKILL WIS HAS BEEN UPGRADED')
            basis.update_skill(user_id, basis.SkillType.WIS, int(points))

    await query.message.reply_text('''Очки распределены''')
    # print(stage)
    match stage:
        case 'GET_EMAIL':
            # await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text(t.get_email_message)
            return GET_EMAIL
        case 'GET_NUMBER':
            # await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text(t.get_number_message)
            return GET_NUMBER
        case 'QUESTION_1':
            keyboard = [
                [
                    InlineKeyboardButton(t.first_question_answers[0], callback_data='q1_1'),
                ],
                [
                    InlineKeyboardButton(t.first_question_answers[1], callback_data='q1_2'),
                ],
                [
                    InlineKeyboardButton(t.first_question_answers[2], callback_data='q1_2'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(t.first_question, reply_markup=reply_markup)
            return QUESTION_1
        case 'QUESTION_2':
            keyboard = [
                [
                    InlineKeyboardButton(t.second_question_answers[0], callback_data='q1_1'),
                ],
                [
                    InlineKeyboardButton(t.second_question_answers[1], callback_data='q1_2'),
                ],
                [
                    InlineKeyboardButton(t.second_question_answers[2], callback_data='q1_3'),
                ],
                [
                    InlineKeyboardButton(t.second_question_answers[3], callback_data='q1_3'),
                ],
                [
                    InlineKeyboardButton(t.second_question_answers[4], callback_data='q1_3'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(t.second_question, reply_markup=reply_markup)
            return QUESTION_2
        case 'QUESTION_3':
            keyboard = [
                [
                    InlineKeyboardButton(t.third_question_answers[0], callback_data='q1_1'),
                    InlineKeyboardButton(t.third_question_answers[1], callback_data='q1_2'),
                ],
                [
                    InlineKeyboardButton(t.third_question_answers[2], callback_data='q1_3'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(t.third_question, reply_markup=reply_markup)
            return QUESTION_3
        case 'QUESTION_4':
            # await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text(t.forth_question)
            return QUESTION_4
        case 'AR':
            # print('Redeem AR code')
            await query.message.reply_text('''Код от AR введен''')
            user_id = update.effective_user.id
            player_data = basis.get_character_data(user_id)
            image_url, caption_text = define_stats(player_data, user_id)
            keyboard = [
                [
                    InlineKeyboardButton("Дальше", callback_data="Дальше"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if player_data:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption_text, reply_markup=reply_markup)
            else:
                pass
            # await query.message.reply_text(t.final_message)
            return END
        case 'BEFORE_AR':
            keyboard = [
                [
                    InlineKeyboardButton('Ввести код', callback_data='enter_ar_code'),
                ],
                [
                    InlineKeyboardButton('Пропустить', callback_data='ar_skip'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.reply_text(t.ar_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
            return AR

def decode_kill_counter(encrypted_string):
    if len(encrypted_string) != 9 or not encrypted_string.startswith(('AR', 'WH')):
        return (None, None)  # Недопустимый формат строки

    try:
        key = int(encrypted_string[2])
    except ValueError:
        return (None, None)

    mapping_table = 'CIYDTFHQXWLGKNPZRVAUEBMJOS'

    def decrypt_digit_pair(encrypted_pair, offset1, offset2):
        try:
            first_char_index = (mapping_table.index(encrypted_pair[0]) - key - offset1 + 26) % 26
            second_char_index = (mapping_table.index(encrypted_pair[1]) - key - offset2 + 26) % 26
            # Проверяем, что оба символа соответствуют одному и тому же числу
            if first_char_index != second_char_index:
                return None
            return first_char_index
        except ValueError:
            return None

    decrypted_digits = []
    for i in range(3, 9, 2):
        decrypted_digit = decrypt_digit_pair(encrypted_string[i:i+2], 7 if i == 3 else 2 if i == 5 else 3, 3 if i == 3 else 1 if i == 5 else 6)
        if decrypted_digit is None:  # Если дешифровка не удалась
            return (None, None)
        decrypted_digits.append(decrypted_digit)

    # Сборка дешифрованного числа
    decrypted_num = decrypted_digits[0] * 100 + decrypted_digits[1] * 10 + decrypted_digits[2]
    return (decrypted_num, encrypted_string[:2])

def check_user_input(user_input, user_id):
    parts = user_input
    encrypted_string = parts
    decrypted_score, activity_type = decode_kill_counter(encrypted_string)
    # print(decrypted_score, activity_type)
    if activity_type == 'AR':  # Проверяем, соответствует ли тип активности
        return [decrypted_score, activity_type]
    elif activity_type == 'WH':
        return [decrypted_score, activity_type]
    else:
        return [None, None]

async def code_capsule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id

    # points, type = check_user_input(user_input, user_id)
    if user_input == CAPSULE_CODE:
        points = random.randint(1, 3)
        basis.event_completed(user_id, EventType.WHEEL)
        keyboard = [
            [
                InlineKeyboardButton('Сила', callback_data=f'{points}-QUESTION_1-skill_STR'),
                InlineKeyboardButton('Ловкость', callback_data=f'{points}-QUESTION_1-skill_AGL'),
            ],
            [
                InlineKeyboardButton('Интеллект', callback_data=f'{points}-QUESTION_1-skill_WIS'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        # await update.callback_query.edit_message_reply_markup(None)
        await update.message.reply_text(f'''Отлично, выбери характеристику, которую улучшишь на +{points}''', reply_markup=reply_markup)
        return DISTRIBUTE
    else:
        keyboard = [
            [
                InlineKeyboardButton('Назад', callback_data=f'QUESTION_1-back-CAPSULE'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('''Неверно, введи код снова или вернись назад''', reply_markup=reply_markup)

async def code_ar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user_id = update.effective_user.id

    points, type = check_user_input(user_input, user_id)

    if points and type == 'AR':
        basis.event_completed(user_id, EventType.AR)
        basis.add_ar_points(user_id, points)
        await update.message.reply_text(f'''Отлично, ты заработал {points} баллов''')
        player_data = basis.get_character_data(user_id)
        if player_data:
            image_url, caption_text = define_stats(player_data, user_id)
            keyboard = [
                [
                    InlineKeyboardButton("Дальше", callback_data="Дальше"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption_text, reply_markup=reply_markup)
            return END
    else:
        keyboard = [
            [
                InlineKeyboardButton('Назад', callback_data=f'END-back-AR'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('''Неверно, введи код снова или вернись назад''', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        #print('BACK')
        if query.data == 'QUESTION_1-back-CAPSULE':
            keyboard = [
                [
                    InlineKeyboardButton(t.first_question_answers[0], callback_data='q1_1'),
                ],
                [
                    InlineKeyboardButton(t.first_question_answers[1], callback_data='q1_2'),
                ],
                [
                    InlineKeyboardButton(t.first_question_answers[2], callback_data='q1_2'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_reply_markup(None)

            await query.message.reply_text(t.first_question, reply_markup=reply_markup)
            return QUESTION_1
        if query.data == 'END-back-AR':
            user_id = update.effective_user.id
            player_data = basis.get_character_data(user_id)
            image_url, caption_text = define_stats(player_data, user_id)
            keyboard = [
                [
                    InlineKeyboardButton("Дальше", callback_data="Дальше"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_reply_markup(None)
            if player_data:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption_text, reply_markup=reply_markup)
            else:
                pass
            # await query.message.reply_text(t.final_message)
            return END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    player_data = basis.get_character_data(user_id)
    image_url, caption_text = define_stats(player_data, user_id)

    if player_data:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption_text)

async def send_message_to_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text_after_command = ' '.join(context.args)
    # get all users
    user_ids = basis.get_all_users_tg_id()
    #print(user_ids)
    user_id = update.effective_user.id
    message = text_after_command
    if user_id in ALLOWED_USER_IDS:
        for user_id in user_ids:
            try:
                await context.bot.send_message(chat_id=user_id['chat_id'], text=message)
            except:
                pass
                # print('invalid')
    else:
        pass
        # print('У вас нет доступа для рассылки сообщений всем пользователям')

async def send_message_to_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    args = context.args
    user_id = update.effective_user.id
    users_data = basis.get_all_users_tg_id()
    #print(users_data)
    if user_id in ALLOWED_USER_IDS:
        for nickname in args:
            user_data = next((user for user in users_data if user['username'] == nickname), None)

            # If user_data is None, the provided nickname doesn't exist in your database
            if user_data is None:
                #print(f"User with nickname '{nickname}' not found.")
                continue

            # Extract chat_id from user_data and send the message
            chat_id = user_data['chat_id']
            message = 'Вы прошли в финал\nПодойдите к стенду Базис, чтобы принять участие в супер игре'
            try:
                await context.bot.send_message(chat_id=chat_id, text='🎲')
                await context.bot.send_message(chat_id=chat_id, text=message)
                print(f"Message sent to user '{nickname}' with chat ID '{chat_id}'.")
            except Exception as e:
                print(f"Failed to send message to user '{nickname}' with chat ID '{chat_id}': {e}")
    else:
        print('У вас нет доступа для отправки сообщения конкретным пользователям')

async def ar_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    character_data = basis.get_character_data(user_id)
    activities_finished = character_data['activities_finished']
    if activities_finished['AR']:
        await update.message.reply_text('''Вы уже вводили код от AR''')
    else:
        await update.message.reply_text('''Введите код от AR: ''')

async def capsule_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    character_data = basis.get_character_data(user_id)
    activities_finished = character_data['activities_finished']
    if activities_finished['WHEEL']:
        await update.message.reply_text('''Вы уже вводили код от капсулы''')
    else:
        await update.message.reply_text('''Введите код от капсулы: ''')

async def code_ar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # print('ENTER AR CODE')
    user_id = update.effective_user.id
    character_data = basis.get_character_data(user_id)
    activities_finished = character_data['activities_finished']
    # print(activities_finished)
    user_input = update.message.text
    user_id = update.effective_user.id

    points, type = check_user_input(user_input, user_id)
    if points and type == 'AR' and not activities_finished['AR']:
        basis.event_completed(user_id, EventType.AR)
        basis.add_ar_points(user_id, points)
        await update.message.reply_text(f'''Отлично, ты заработал {points} баллов''')
    elif activities_finished['AR']:
        await update.message.reply_text('''Ты уже проходил квест AR''')
    else:
        await update.message.reply_text('''Код неверный''')

async def code_capsule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    character_data = basis.get_character_data(user_id)
    activities_finished = character_data['activities_finished']
    # print(activities_finished)
    user_input = update.message.text
    user_id = update.effective_user.id
    # print(user_input)
    if user_input == CAPSULE_CODE:
        points = random.randint(1, 3)
        basis.event_completed(user_id, EventType.WHEEL)
        keyboard = [
            [
                InlineKeyboardButton('Сила', callback_data=f'{points}-CAPSULE_COMMAND-skill_STR'),
                InlineKeyboardButton('Ловкость', callback_data=f'{points}-CAPSULE_COMMAND-skill_AGL'),
            ],
            [
                InlineKeyboardButton('Интеллект', callback_data=f'{points}-CAPSULE_COMMAND-skill_WIS'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f'''Отлично, выбери характеристику, которую улучшишь на +{points}''', reply_markup=reply_markup)
    elif activities_finished['WHEEL']:
        await update.message.reply_text('''Ты уже вводил код от капсулы''')
    else:
        await update.message.reply_text('''Код неверный''')

async def left_queries(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    points_quest = None
    quest = None
    answer = None
    try:
        points_quest, quest, answer = query.data.split('-')
    except:
        pass

    if query.data == "boss-spend-points":
        # basis.spend_points(user_id, points)
        player_data = basis.get_character_data(user_id)
        if player_data:
            points = player_data['total_skill_points']
            converted_point = points / 10
            keyboard = [
                [
                    InlineKeyboardButton('Сила', callback_data=f'{converted_point}-BOSS-skill_STR_BOSS'),
                    InlineKeyboardButton('Ловкость', callback_data=f'{converted_point}-BOSS-skill_AGL_BOSS'),
                ],
                [
                    InlineKeyboardButton('Интеллект', callback_data=f'{converted_point}-BOSS-skill_WIS_BOSS'),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_reply_markup(None)
            await query.message.reply_text(f'''Отлично, выбери характеристику, которую хочешь прокачать БОССУ на +{converted_point}''', reply_markup=reply_markup)
    elif quest == 'CAPSULE_COMMAND' and (answer == 'skill_STR' or answer == 'skill_AGL' or answer == 'skill_WIS'):
        print(basis.get_character_data(user_id))
        match answer:
            case 'skill_STR':
                #print('SKILL STR HAS BEEN UPGRADED')
                basis.update_skill(user_id, basis.SkillType.STR, int(points_quest))
                # print(basis.get_character_data(user_id))
            case 'skill_AGL':
                #print('SKILL AGL HAS BEEN UPGRADED')
                basis.update_skill(user_id, basis.SkillType.AGL, int(points_quest))
                # print(basis.get_character_data(user_id))
            case 'skill_WIS':
                #print('SKILL WIS HAS BEEN UPGRADED')
                basis.update_skill(user_id, basis.SkillType.WIS, int(points_quest))
                # print(basis.get_character_data(user_id))
        if quest == "AR":
            basis.event_completed(user_id, EventType.AR)
        elif quest == 'WH':
            basis.event_completed(user_id, EventType.WHEEL)
        await update.callback_query.edit_message_reply_markup(None)
        await query.message.reply_text(f'Очки распределены')
    elif answer == 'skill_STR_BOSS' or answer == 'skill_AGL_BOSS' or answer == 'skill_WIS_BOSS':
        match answer:
            case 'skill_STR_BOSS':
                basis.spend_points(user_id, points_quest, basis.SkillType.STR)
            case 'skill_AGL_BOSS':
                basis.spend_points(user_id, points_quest, basis.SkillType.AGL)
            case 'skill_WIS_BOSS':
                basis.spend_points(user_id, points_quest, basis.SkillType.WIS)
        await update.callback_query.edit_message_reply_markup(None)
        await query.message.reply_text(f'Ты улучшил главного БОССА на +{points_quest}')

async def start_final_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global IS_ROUND
    user_id = update.effective_user.id

    if user_id in ALLOWED_USER_IDS:
        print('финальная игра началась')
        keyboard = [
            [
                InlineKeyboardButton("Потратить очки💸", callback_data="boss-spend-points"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        users = basis.get_top_users()

        for user in users:
            points = user['total_skill_points']
            try:
                await context.bot.send_message(chat_id=user['chat_id'], text=f'Началась финальная игра, ты можешь помочь БОССУ победить. Трать свои очки, чтобы прокачать его. Очки конвертируются 10 к 1. Твои 10 очков дадут БОССУ +1\nУ тебя есть {points}', reply_markup=reply_markup)
            except Exception as e:
                # print(f"Error sending message to user {user['chat_id']}: {e}")
                pass
        IS_ROUND = True
    else:
        print('У вас нет доступа для начала финальной игры')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={

            INTRO1:             [CallbackQueryHandler(intro1)],
            CHOOSE_RACE:        [CallbackQueryHandler(choose_race)],
            INTRO2:             [CallbackQueryHandler(intro2)],
            CHOOSE_CLASS:       [CallbackQueryHandler(choose_class)],
            CAPSULE:            [CallbackQueryHandler(capsule)],
            HANDLE_CAPSULE:     [CallbackQueryHandler(handle_capsule)],
            INTRO3:             [CallbackQueryHandler(intro3)],
            QUESTION_1:         [CallbackQueryHandler(question1)],
            GET_EMAIL:      [
                MessageHandler(
                    filters.Regex(".*"), get_email
                ),
            ],
            QUESTION_2:         [CallbackQueryHandler(question2)],
            GET_NUMBER:      [
                MessageHandler(
                    filters.Regex(".*"), get_number
                ),
            ],
            QUESTION_3:         [CallbackQueryHandler(question3)],
            QUESTION_4:         [
                MessageHandler(
                    filters.Regex(".*"), question4
                ),
            ],
            AR:                 [CallbackQueryHandler(ar)],
            END:         [CallbackQueryHandler(end)],
            DISTRIBUTE:     [CallbackQueryHandler(distribute)],
            CODE_CAPSULE:     [
                MessageHandler(
                    filters.Regex(".*"), code_capsule
                ),
            ],
            CODE_AR:     [
                MessageHandler(
                    filters.Regex(".*"), code_ar
                ),
            ],

        },
        fallbacks=[
            CallbackQueryHandler(button),
            ],
        per_user=True
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stats', stats))

    # handle ar and capsule code collecting
    application.add_handler(CommandHandler('ar', ar_code_command))
    application.add_handler(CommandHandler('capsule', capsule_code_command))
    application.add_handler(MessageHandler(
                    filters.Regex(r'^AR'), code_ar_command
                ),)
    application.add_handler(MessageHandler(
                    filters.Regex(r'^WH'), code_capsule_command
                ),)

    application.add_handler(CallbackQueryHandler(left_queries))

    # DANGER ZONE
    application.add_handler(CommandHandler('send_message_to_all', send_message_to_all))
    application.add_handler(CommandHandler('send_message_to_users', send_message_to_users))
    application.add_handler(CommandHandler('start_final_game', start_final_game))

    # application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
