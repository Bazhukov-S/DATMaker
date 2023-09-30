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


"""
Добавить ввод всех параметров одним сообщением
"""

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