import json
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

from utils import CommandExecutor, Parser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def button(update: Update, context: CallbackContext) -> None:
	query = update.callback_query
	query.answer()
	data = query.data

	past_reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать прошедшие", callback_data='htmore')]])

	if data.startswith('b'):
		query.edit_message_text(text=Parser.books(int(data.split('_')[1])), parse_mode='HTML')
	elif data == 'htmore':
		parser = Parser.Parser(int(query.message.text[:2]))
		query.edit_message_text(text=f'{query.message.text_html}\n\n<b>Идет загрузка прошедших заданий...\nПожалуйста, подождите.</b>', parse_mode='HTML')
		parser.parse_prev_ht(query.message.text.count('Прошедшие задания'))
		query.edit_message_text(text=f'{query.message.text_html}\n\n<b>Прошедшие задания</b>\n{parser.format_page()}', parse_mode='HTML', reply_markup=past_reply_markup)
	elif data.startswith('ht'):
		query.edit_message_text(text=f'\n<b>Идет загрузка...\nПожалуйста, подождите.</b>', parse_mode='HTML')
		parser = Parser.Parser(int(data.split('_')[1]))
		parser.parse_current_ht()
		query.edit_message_text(text=parser.format_page(), reply_markup=past_reply_markup, parse_mode='HTML')

def main():
	updater = Updater(json.load(open("secret.json"))["token"], use_context=True)
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
