
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes, Application
from jinja2 import Environment, FileSystemLoader

# Чтение содержимого шаблона из файла
template_loader = FileSystemLoader(searchpath="./")
template_env = Environment(loader=template_loader)
template = template_env.get_template("E:\study\Maker_DAT_BOT\BOXTemplate\INCLUDE\BOSTemplate_PROPS.inc")

# Функция-обработчик команды /start
def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Введи значение параметра Density_OIL:")

# Функция-обработчик для получения значения параметра Density_OIL от пользователя и отправки файла
def process_density_oil(update, context):
    chat_id = update.message.chat_id
    density_oil = update.message.text

    try:
        # Рендеринг шаблона с полученным значением параметра Density_OIL
        rendered_template = template.render(Density_OIL=density_oil)

        # Запись результата в файл
        with open("E:\study\Maker_DAT_BOT\BOXTemplate\INCLUDE\BOSTemplate_PROPS.inc", "w") as file:
            file.write(rendered_template)

        # Отправка файла пользователю
        context.bot.send_document(chat_id=chat_id, document=open("E:\study\Maker_DAT_BOT\BOXTemplate\INCLUDE\BOSTemplate_PROPS.inc", "rb"))

    except Exception as e:
        # Если возникла ошибка
        context.bot.send_message(chat_id=chat_id, text=f"Произошла ошибка: {str(e)}")

def main():
 
    dp = Application.builder().token("6593404619:AAEMwvBPipD9_w76tspKiLC1hDzoPZ0Pnbk").build()

    # Добавление обработчиков
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.UpdateFilter, process_density_oil))

    dp.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == '__main__':
    main()


