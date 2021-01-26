import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

import secret
from utils import CommandExecutor, Parser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def button(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.answer()
	data = query.data

	if data == 'b10':
		query.edit_message_text(text=Parser.books(10), parse_mode='HTML')
	elif data == 'b9':
		query.edit_message_text(text=Parser.books(9), parse_mode='HTML')
	elif data == 'ht10':
		query.edit_message_text(text=Parser.hometasks(10), parse_mode='HTML')
	elif data == 'ht9':
		query.edit_message_text(text=Parser.hometasks(9), parse_mode='HTML')

def main():
	updater = Updater(secret.token, use_context=True)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('hometasks', CommandExecutor.hometasks_command))
	dispatcher.add_handler(CommandHandler('stats', CommandExecutor.stats_command))
	dispatcher.add_handler(CommandHandler('coronavirus', CommandExecutor.coronavirus_command))
	dispatcher.add_handler(CommandHandler('books', CommandExecutor.books_command))
	dispatcher.add_handler(CommandHandler('say', CommandExecutor.say_command))
	dispatcher.add_handler(CommandHandler('help', CommandExecutor.help_command))
	dispatcher.add_handler(CommandHandler('start', CommandExecutor.help_command))
	dispatcher.add_handler(CallbackQueryHandler(button))
	dispatcher.add_handler(MessageHandler(Filters.text, CommandExecutor.message_handler))

	updater.start_polling()


if __name__ == '__main__':
	main()
