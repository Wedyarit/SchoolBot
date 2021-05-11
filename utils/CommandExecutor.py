import json
import random
import time
from threading import Thread, Timer

import requests
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def hometasks_command(update: Update, context: CallbackContext) -> None:
	keyboard = [[]]
	for i, auth in enumerate(json.loads(open('secret.json', 'r').read())["auth"]):
		if i % 2 == 0:
			keyboard[int(i / 2)].append(InlineKeyboardButton(f'{auth["form"]} класс', callback_data=f'ht_{auth["form"]}'))
		else:
			keyboard.append([InlineKeyboardButton(f'{auth["form"]} класс', callback_data=f'ht_{auth["form"]}')])
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(reply_to_message_id=update.message.message_id, text='Выберите класс:', reply_markup=reply_markup)

def books_command(update: Update, context: CallbackContext) -> None:
	keyboard = [[InlineKeyboardButton("10 класс", callback_data='b_10'), InlineKeyboardButton("9 класс", callback_data='b_9')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(reply_to_message_id=update.message.message_id, text='Выберите класс:', reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(reply_to_message_id=update.message.message_id, text=f"Приветствую, <b>{update.message.from_user.first_name}</b>, добро пожаловать! \n📄 <b>Список доступных Вам команд:</b> 📄\n/hometasks - Домашняя работа на неделю; \n/books - Список виртуальных учебников; \n/coronavirus - Статистика распространения пандемии; \n/help - Список доступных Вам команд;", parse_mode='HTML')

def stats_command(update: Update, context: CallbackContext) -> None:
	if update.message.chat.id != json.load(open("secret.json"))["group_id"]:
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

def delete_message_after(mes, after_seconds, update: Update):
	time.sleep(after_seconds)
	update.message.bot.deleteMessage(update.message.chat_id, mes.message_id)

def say_command(update: Update, context: CallbackContext) -> None:
	if update.message.from_user.id == 856066035:
		update.message.bot.send_message(chat_id=update.message.chat_id, text=update.message.text[4:], parse_mode='HTML', disable_web_page_preview=True)
		update.message.delete()

def message_handler(update: Update, context: CallbackContext):
	msg = update.message.text.lower()

	if update.message.chat.id != json.load(open("secret.json"))["group_id"]:
		return

	file = open("resources/phrases.json", encoding="utf8")
	phrases = json.load(file)
	file.close()

	if random.randint(0, 100) < 2:
		Thread(target=delete_message_after, args=(update.message.reply_text(reply_to_message_id=update.message.message_id, text=random.choice(phrases[0]["phrases"])), 30, update)).start()
		return

	for phrase in phrases:
		for trigger in phrase["triggers"]:
			if trigger in msg:
				Thread(target=delete_message_after, args=(update.message.reply_text(reply_to_message_id=update.message.message_id, text=random.choice(phrase["phrases"])), 30, update)).start()
				Thread(target=delete_message_after, args=(update.message.reply_photo(random.choice(phrase["photos"])), 30, update)).start()
				return
