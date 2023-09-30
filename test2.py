"""
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    Updater
)
from jinja2 import Environment, FileSystemLoader


app = Flask(__name__)
jinja_env = Environment(loader=FileSystemLoader('.'))
template_file = "C:\УЧЕБА\DATMaker_BOT\DATMaker\BOXTemplate\INCLUDE\BOSTemplate_PROPS.inc"
output_file = "C:\УЧЕБА\DATMaker_BOT\DATMaker\BOXTemplate\INCLUDE\BOSTemplate_PROPS_.inc"


# def render_template(template_data):
#     template = jinja_env.get_template(template_file)
#     output = template.render(template_data)
#     with open(output_file, 'w') as f:
#         f.write(output)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Введите значение параметра Density_OIL:')


def process_text(update: Update, context: CallbackContext) -> None:
    density_oil = update.message.text

    # Можно добавить валидацию значения density_oil здесь

    # template_data = {'Density_OIL': density_oil}
    # render_template(template_data)

    # Отправка файла пользователю
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(template_file, 'rb'))


app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route(f'/{"6593404619:AAEMwvBPipD9_w76tspKiLC1hDzoPZ0Pnbk"}', methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return 'ok'


if __name__ == '__main__':
    # Здесь необходимо заменить 'YOUR_BOT_TOKEN' на соответствующий токен вашего бота
    updater = Updater(token='6593404619:AAEMwvBPipD9_w76tspKiLC1hDzoPZ0Pnbk', use_context=True)
    bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_text))

    updater.start_polling()
    app.run(threaded=True)
"""

import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Инициализация логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Определение состояний разговора
GRID_SIZE, BLOCK_SIZE, PERMEABILITY, POROSITY, NTG, CREATE_MODEL = range(6)


def start(update, context):
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text(
        'Welcome! Do you want to create a model?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CREATE_MODEL


def create_model(update, context):
    user_input = update.message.text
    reply_keyboard = [['Yes', 'No']]
    if user_input == 'Yes':
        context.user_data.clear()
        update.message.reply_text('Please enter the grid size:')
        return GRID_SIZE
    elif user_input == 'No':
        context.user_data.clear()
        update.message.reply_text('Values have been cleared. Do you want to create a model again?',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return CREATE_MODEL


def get_grid_size(update, context):
    grid_size = update.message.text
    context.user_data['Grid Size'] = grid_size
    update.message.reply_text('Please enter the cell size:')
    return BLOCK_SIZE


def get_cell_size(update, context):
    cell_size = update.message.text
    context.user_data['Cell Size'] = cell_size
    update.message.reply_text('Please enter the permeability:')
    return PERMEABILITY


def get_permeability(update, context):
    permeability = update.message.text
    context.user_data['Permeability'] = permeability
    update.message.reply_text('Please enter the porosity:')
    return POROSITY


def get_porosity(update, context):
    porosity = update.message.text
    context.user_data['Porosity'] = porosity
    update.message.reply_text('Please enter the NTG:')
    return NTG


def get_ntg(update, context):
    ntg = update.message.text
    context.user_data['NTG'] = ntg
    create_txt_file(update, context)
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text('Model parameters have been saved. Do you want to create another model?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CREATE_MODEL


def create_txt_file(update, context):
    file_contents = '\n'.join([f'{key}: {value}' for key, value in context.user_data.items()])
    with open('model_parameters.txt', 'w') as file:
        file.write(file_contents)
    file = open("model_parameters.txt", "r")
    update.message.reply_text('Here is your model parameters file:')
    update.message.reply_document(document=file)
    file.close()


def cancel(update, context):
    context.user_data.clear()
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text('Canceled. Do you want to create a model?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CREATE_MODEL


def main():
    updater = Updater("6593404619:AAEMwvBPipD9_w76tspKiLC1hDzoPZ0Pnbk", use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CREATE_MODEL: [MessageHandler(Filters.regex('^(Yes|No)$'), create_model)],
            GRID_SIZE: [MessageHandler(Filters.text, get_grid_size)],
            BLOCK_SIZE: [MessageHandler(Filters.text, get_cell_size)],
            PERMEABILITY: [MessageHandler(Filters.text, get_permeability)],
            POROSITY: [MessageHandler(Filters.text, get_porosity)],
            NTG: [MessageHandler(Filters.text, get_ntg)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()