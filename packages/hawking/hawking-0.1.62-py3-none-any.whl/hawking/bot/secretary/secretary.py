""" Secretary Telegram Bot. """
import logging
import os
import sys
import click

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from hawking.frontend.engine.local import LocalSearchEngine

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

engine = None


def start(update, context):
    log.info("Conversation started!")
    update.message.reply_text('Welcome, secretary started following this conversation.')


def help(update, context):
    log.info("Help requested!")
    update.message.reply_text("I'm listening to conversation and taking notes. If you want to lookup details, send /q <term>")


def question(update, context):
    if update.message == None:
        return

    if update.message.text == None:
        return

    namespace = "secretary_"+str(update.message.chat.id)
    query = update.message.text
    if query.startswith("/q"):
        query = query[len("/q"):]
        query = query.strip()

    log.info('search within "%s" namespace for "%s"', namespace, query)

    results = engine.search(namespace, 3, query)

    chat_id = update.message.chat.id
    for result in results:
        context.bot.send_message(chat_id, text="Score: " + str(result[1]), parse_mode='MARKDOWN', reply_to_message_id=result[0])


def process(update, context):
    if update.message == None:
        return

    if update.message.message_id == None:
        return

    if update.message.text == None:
        return

    phrase = ""
    if update.message.reply_to_message != None:
        if update.message.reply_to_message.text != None:
            phrase += update.message.reply_to_message.text
    phrase += update.message.text

    namespace = "secretary_"+str(update.message.chat.id)
    reference = str(update.message.message_id)

    if engine.index(namespace, reference, phrase):
        log.info("%s/%s, %s inserted", namespace, reference, phrase)
    else:
        log.info("%s/%s, %s updated", namespace, reference, phrase)


def process_entity(update, context):
    log.info(update)


def error(update, context):
    log.warning('"%s" error "%s"', update, context.error)


def serve(bot_token=None):
    if bot_token is None and "SECRETARY_BOT_TOKEN" not in os.environ:
        log.error("Environment variable SECRETARY_BOT_TOKEN not defined, bot won't start!")
        return None

    if os.environ.get("SECRETARY_BOT_TOKEN") is not None:
        bot_token = os.environ["SECRETARY_BOT_TOKEN"]
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("q", question))
    dp.add_handler(MessageHandler(Filters.text, process))
    dp.add_handler(MessageHandler(Filters.sticker, process_entity))
    dp.add_error_handler(error)

    print('Started bot service ...')
    updater.start_polling()
    return updater


def main(queue_path='/tmp'):
    global engine
    engine = LocalSearchEngine(queue_path)
    updater = serve()
    if updater is not None:
        updater.idle()


@click.command()
@click.option('--queue-path', help="Queue dir for stuff.", default="/tmp")
def cli(queue_path):
    main(queue_path)


if __name__ == '__main__':
    cli()
