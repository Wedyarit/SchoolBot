import datetime
import json
import requests

import bs4

from utils.Dates import today, tomorrow, after_tomorrow, weekday

class Parser:
	def __init__(self, form):
		self.form = form
		self.tooltip = True
		self.session = requests.Session()
		self.page = None

		self.authorize()

	def authorize(self):
		data = json.load(open("secret.json", encoding='utf-8'))
		self.session.post(url="http://best.yos.kz/cabinet/", data={"login":next(auth for auth in data["auth"] if auth["form"] == self.form)["login"], "password":next(auth for auth in data["auth"] if auth["form"] == self.form)["password"]})

	def parse_current_ht(self):
		self.page = bs4.BeautifulSoup(self.session.get("http://best.yos.kz/cabinet/?module=diary&part=homeworks").text, "html.parser")

	def parse_prev_ht(self, page):
		self.tooltip = False
		self.page = bs4.BeautifulSoup(self.session.get(f"http://best.yos.kz/cabinet/", params={"module":"diary", "part":"homeworks", "action":"preload", "id":"0", "page":page}, headers={"X-Requested-With":"XMLHttpRequest", "Cookie":f"_ym_d={self.session.cookies.get('_ym_d')}; _ym_uid={self.session.cookies.get('_ym_uid')}; _ym_isad={self.session.cookies.get('_ym_isad')}; __jsessid={self.session.cookies.get('__jsessid')}", "Referer":"http://best.yos.kz/cabinet/?module=diary&part=homeworks", "Host":"best.yos.kz"}).text, "html.parser")

	def format_page(self):
		result = []

		if self.tooltip:
			result = [f"<b>{self.form} класс</b>"]

		table_title = self.page.findAll("td", {"class":"hw-title"})
		table_pole = self.page.select(".hw-table")

		stable_date = ""

		for table_pole_res in table_pole[1:]:
			for table in table_pole_res.findAll("tr", {"class":"cl-row"}):

				tab = table.findAll("td")
				date = table_title[table_pole.index(table_pole_res) - 1].getText().replace("\n", "")
				if not date.startswith(" "):
					date = date[4:]
				date = date[:10]

				if stable_date != date:
					result.append(f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<b>{date}г.</b>")
					stable_date = date

					if date == today().strftime("%d.%m.%Y"):
						today_day = today()
						result.append(f"📚  <i>Сегодня - {weekday(today_day.weekday())}</i>  📚")
					elif date == tomorrow().strftime("%d.%m.%Y"):
						tomorrow_day = tomorrow()
						result.append(f"🧨 <i>Завтра - {weekday(tomorrow_day.weekday())}</i> 🧨")
					elif date == after_tomorrow().strftime("%d.%m.%Y"):
						after_tomorrow_day = after_tomorrow()
						result.append(f"📋 <i>Послезавтра - {weekday(after_tomorrow_day.weekday())}</i>  📋")
					else:
						date_time_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
						result.append(f"📆 <i>{weekday(date_time_obj.weekday())}</i> 📆")

				result.append(f"➜ <u>{tab[1].getText()}:</u>")

				if tab[2].getText().endswith("!") or tab[2].getText().endswith(".") or tab[2].getText().endswith(";") or tab[2].getText().endswith(","):
					result.append(f"    {tab[2].getText()[0].upper() + tab[2].getText()[:-1][1:]};")
				else:
					result.append(f"    {tab[2].getText()[0].upper() + tab[2].getText()[1:]};")

				for a in table.find_all('a', href=True):
					if len(a['href']) > 1:
						result.append(f'  📎 <a href="http://best.yos.kz/cabinet/{a["href"]}">{a.getText()[0].upper() + a.getText()[1:]}</a>')

		result.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

		if len(result) <= 3:
			result.append("<b>Домашняя работа отсутствует.</b>")
			result.append("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

		return "\n".join(result)

def books(form):
	file = open("resources/books.json", encoding='utf8')
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
