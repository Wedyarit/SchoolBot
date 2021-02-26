import json
import random
from threading import Thread, Timer

import requests
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import secret

def hometasks_command(update: Update, context: CallbackContext) -> None:
	keyboard = [[InlineKeyboardButton("10 класс", callback_data='ht10'), InlineKeyboardButton("7 класс", callback_data='ht7'), ]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(reply_to_message_id=update.message.message_id, text='Выберите класс:', reply_markup=reply_markup)

def books_command(update: Update, context: CallbackContext) -> None:
	keyboard = [[InlineKeyboardButton("10 класс", callback_data='b10'), InlineKeyboardButton("9 класс", callback_data='b9'), ]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(reply_to_message_id=update.message.message_id, text='Выберите класс:', reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(reply_to_message_id=update.message.message_id, text=f"Приветствую, <b>{update.message.from_user.first_name}</b>, добро пожаловать! \n📄 <b>Список доступных Вам команд:</b> 📄\n/hometasks - Домашняя работа на неделю; \n/books - Список виртуальных учебников; \n/coronavirus - Статистика распространения пандемии; \n/help - Список доступных Вам команд;", parse_mode='HTML')

def stats_command(update: Update, context: CallbackContext) -> None:
	if update.message.chat.id != secret.group_id:
		return

	file = open("../resources/phrases.json", encoding="utf8")
	phrases = json.load(file)
	file.close()

	all_photos = 0
	all_phrases = 0
	all_triggers = 0

	output_text = "***Статистика фраз: ***"

	for object in phrases:
		all_phrases += len(object["phrases"])
		all_triggers += len(object["triggers"])
		all_photos += len(object["photos"])

		output_text += "\n***" + object["name"] + "***:"

		output_text += "\n ➜ Количество фраз: " + str(len(object["phrases"]))
		output_text += "\n ➜ Количество триггеров: " + str(len(object["triggers"]))
		output_text += "\n ➜ Количество фото: " + str(len(object["photos"]))

	output_text += "\n***Итого: *** \n ➜ Всего фраз: " + str(all_phrases) + "\n ➜ Всего триггеров: " + str(all_triggers) + "\n ➜ Всего фото: " + str(all_photos)

	update.message.reply_text(reply_to_message_id=update.message.message_id, text=output_text, parse_mode='Markdown')

def coronavirus_command(update: Update, context: CallbackContext) -> None:
	kazakhstan_data = json.loads(requests.get('https://api.covid19api.com/total/country/Kazakhstan').text)[-1]
	world_data = json.loads(requests.get('https://api.covid19api.com/summary').text).get('Global')

	message_content = f'🦠 <b>Статистика распространения Covid19</b> 🦠\n<b>Казахстан:</b>\n ➜ Подтвержденных случаев: {kazakhstan_data.get("Confirmed")}\n ➜ Смертей: {kazakhstan_data.get("Deaths")}\n ➜ Выздоровевших: {kazakhstan_data.get("Recovered")}\n ➜ Активно заражены: {kazakhstan_data.get("Active")}\n<b>Мир:</b>\n ➜ Новых подтвержденных случаев: {world_data.get("NewConfirmed")}\n ➜ Всего подтвержденных случаев: {world_data.get("TotalConfirmed")}\n ➜ Новых смертей: {world_data.get("NewDeaths")}\n ➜ Всего смертей: {world_data.get("TotalDeaths")}\n ➜ Новых выздоровевших: {world_data.get("NewRecovered")}\n ➜ Всего выздоровевших: {world_data.get("TotalRecovered")}'
	update.message.reply_text(reply_to_message_id=update.message.message_id, text=message_content, parse_mode='HTML')


data = []

def antiflood(user_id, chat_id, update : Update):
	counter = 0
	msg_ids = []
	for idx, item in enumerate(data):
		combined = chat_id + ":" + user_id
		if combined in item:
			msg_id = data[idx].split(":")[2]
			msg_ids.append(msg_id)
			counter += 1
	if counter >= 3:
		data.clear()
		print("[!] " + str(user_id) + " флудит в " + str(chat_id))
		update.message.bot.send_message(chat_id, text=f'[{update.message.from_user.first_name}](tg://user?id={user_id}), пожалуйста, не флудите.', parse_mode='Markdown')
		for msg in msg_ids[1:]:
			update.message.bot.deleteMessage(chat_id, int(msg))
	elif counter < 3:
		data.clear()

def message_handler(update: Update, context: CallbackContext):
	string_to_append = str(update.message.chat_id) + ":" + str(update.message.from_user.id) + ":" + str(update.message.message_id)
	data.append(string_to_append)
	Timer(1.5, antiflood, [str(update.message.from_user.id), str(update.message.chat_id), update]).start()

	msg = update.message.text.lower()

	if update.message.chat.id != secret.group_id:
		return

	file = open("resources/phrases.json", encoding="utf8")
	phrases = json.load(file)
	file.close()

	if random.randint(0, 100) < 2:
		update.message.reply_text(reply_to_message_id=update.message.message_id, text=random.choice(phrases[0]["phrases"]))
		return

	for phrase in phrases:
		for trigger in phrase["triggers"]:
			if trigger in msg:
				update.message.reply_text(reply_to_message_id=update.message.message_id, text=random.choice(phrase["phrases"]))
				update.message.reply_photo(random.choice(phrase["photos"]))
				return

def say_command(update: Update, context: CallbackContext) -> None:
	if update.message.from_user.id == 856066035:
		update.message.bot.send_message(chat_id=update.message.chat_id, text=update.message.text[4:], parse_mode='HTML', disable_web_page_preview=True)
		update.message.delete()