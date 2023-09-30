import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from jinja2 import Environment, FileSystemLoader

# Инициализация логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Определение состояний разговора
CREATE_MODEL, GRID_SIZE, NTG, PERM, PERMZ, PORO = range(6)


def start(update, context):
    reply_keyboard = [['ДА', 'Завершить']]
    update.message.reply_text(
        'Если хотите создать модель, нажмите ДА',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CREATE_MODEL


def create_model(update, context):
    reply_keyboard = [['ДА', 'Завершить']]
    user_input = update.message.text
    if user_input == 'ДА':
        context.user_data.clear()
        update.message.reply_text('Введите данные модели в одну строку (NTG, PERM, PORO):\n\n'
                                  'Пример: 0.9 200 0.2')
        return GRID_SIZE
    elif user_input == 'Завершить':
        context.user_data.clear()
        update.message.reply_text('Данные очищены. Хотите снова создать модель?',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return CREATE_MODEL


def get_parameters(update, context):
    parameters = update.message.text.split(' ')
    if len(parameters) != 3:
        update.message.reply_text('Введено неверное количество параметров. Попробуйте снова.')
        return GRID_SIZE
    
    context.user_data['NTG'] = parameters[0]
    context.user_data['PERM'] = parameters[1]
    context.user_data['PORO'] = parameters[2]
    context.user_data['PERMZ'] = str(float(parameters[1]) / 10)
    
    # Создание файла на основе шаблона с помощью Jinja
    env = Environment(loader=FileSystemLoader("./BOXTemplate"))
    template = env.get_template("BOXTEMPLATE.data")
    file_content = template.render(context.user_data)
    
    # Отправка файла пользователю
    file_name = 'DATAMaker_model.data'
    with open(file_name, 'w') as file:
        file.write(file_content)
    
    update.message.reply_document(document=open(file_name, 'rb'))
    update.message.reply_text('Модель создана и отправлена!')
    
    return ConversationHandler.END

def cancel(update, context):
    context.user_data.clear()
    reply_keyboard = [['ДА', 'Завершить']]
    update.message.reply_text('Canceled. Do you want to create a model?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CREATE_MODEL


def main():
    # Создание и настройка объекта updater
    updater = Updater(token='6593404619:AAEMwvBPipD9_w76tspKiLC1hDzoPZ0Pnbk', use_context=True)

    # Получение диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CREATE_MODEL: [MessageHandler(Filters.regex('^(ДА|Завершить)$'), create_model)],
            GRID_SIZE: [MessageHandler(Filters.text, get_parameters)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()


if __name__ == '__main__':
    main()