import datetime
import json

import bs4
import mechanicalsoup

import secret

def weekday(day):
	switcher = {
		0:"Понедельник",
		1:"Вторник",
		2:"Среда",
		3:"Четверг",
		4:"Пятница",
		5:"Суббота",
		6:"Воскресенье"
		}
	return switcher.get(day, "Invalid month")

def today():
	today = datetime.date.today()
	return today
def tomorrow():
	today = datetime.date.today()
	tomorrow = today + datetime.timedelta(days=1)
	return tomorrow
def after_tomorrow():
	today = datetime.date.today()
	after_tomorrow = today + datetime.timedelta(days=2)
	return after_tomorrow

def form_login9():
	browser = mechanicalsoup.StatefulBrowser()
	browser.open("http://best.yos.kz/cabinet/")

	browser.select_form('form[method="post"]')
	browser['login'] = secret.form_login9
	browser['password'] = secret.form_password9
	browser.submit_selected()

	return browser

def form_login6():
	browser = mechanicalsoup.StatefulBrowser()
	browser.open("http://best.yos.kz/cabinet/")

	browser.select_form('form[method="post"]')
	browser['login'] = secret.form_login6
	browser['password'] = secret.form_password6
	browser.submit_selected()

	return browser

def hometasks(key):
	array = []
	browser = None

	if key == 10:
		browser = form_login9()
		array.append("<b>10 класс</b>")
	elif key == 7:
		browser = form_login6()
		array.append("<b>7 класс</b>")

	soup = browser.open_relative("http://best.yos.kz/cabinet/?module=diary&part=homeworks")
	b = bs4.BeautifulSoup(soup.text, "html.parser")
	table_title = b.findAll("td", {
		"class":"hw-title"
		})
	table_pole = b.select(".hw-table")

	stable_date = ""

	for table_pole_res in table_pole[1:]:
		for table in table_pole_res.findAll("tr", {
			"class":"cl-row"
			}):

			tab = table.findAll("td")
			date = table_title[table_pole.index(table_pole_res) - 1].getText().replace("\n", "")
			if not date.startswith(" "):
				date = date[4:]
			date = date[:10]

			if stable_date != date:
				array.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<b>" + date + "г.</b>")
				stable_date = date

				if date == today().strftime("%d.%m.%Y"):
					today_day = today()
					array.append("📚  <i>Сегодня - " + weekday(today_day.weekday()) + "</i>  📚")
				elif date == tomorrow().strftime("%d.%m.%Y"):
					tomorrow_day = tomorrow()
					array.append("🧨 <i>Завтра - " + weekday(tomorrow_day.weekday()) + "</i> 🧨")
				elif date == after_tomorrow().strftime("%d.%m.%Y"):
					after_tomorrow_day = after_tomorrow()
					array.append("📋 <i>Послезавтра - " + weekday(after_tomorrow_day.weekday()) + "</i>  📋")
				else:
					date_time_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
					array.append("📆 <i>" + weekday(date_time_obj.weekday()) + "</i> 📆")

			array.append("➜ <u>" + tab[1].getText() + ":</u>")

			if tab[2].getText().endswith("!") or tab[2].getText().endswith(".") or tab[2].getText().endswith(";") or tab[2].getText().endswith(","):
				array.append("    " + tab[2].getText()[0].upper() + tab[2].getText()[:-1][1:] + ";")
			else:
				array.append("    " + tab[2].getText()[0].upper() + tab[2].getText()[1:] + ";")

			for a in table.find_all('a', href=True):
				if len(a['href']) > 1:
					array.append("  📎 " + '<a href="http://best.yos.kz/cabinet/' + a['href'] + '">' + a.getText()[0].upper() + a.getText()[1:] + '</a>')

	array.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

	if len(array) <= 3:
		array.append("<b>Домашняя работа отсутствует.</b>")
		array.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

	return "\n".join(array)

def books(form):
	file = open("../resources/books.json", encoding='utf8')
	objects = json.load(file)
	file.close()
	result = []
	title = ''

	for object in objects:
		if object['form'] == form:
			title = object['title']
			for book in object['books']:
				if book['url'] is None:
					result.append(book['name'])
				else:
					result.append('<a href="' + book['url'] + '">' + book['name'] + '</a>')
	return title + "\n" + (";\n".join(result)) + "."
