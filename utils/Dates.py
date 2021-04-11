import datetime

def weekday(day):
	return {0:"Понедельник", 1:"Вторник", 2:"Среда", 3:"Четверг", 4:"Пятница", 5:"Суббота", 6:"Воскресенье"}.get(day, "Invalid month")

def today():
	return datetime.date.today()

def tomorrow():
	return datetime.date.today() + datetime.timedelta(days=1)

def after_tomorrow():
	return datetime.date.today() + datetime.timedelta(days=2)