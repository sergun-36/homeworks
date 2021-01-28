import requests

def do_request(url):
	response=requests.get(url)
	if response.status_code in ok_codes:
		result=response.json()
		return result
	else:
		print(f"Запрос вернул ошибку со статусом {response.status_code}")

def add_text(date, delta, message):
	if delta >0:
		message+=f"\n{date}: +{delta}"
		return message
	else:
		message+=f"\n{date}: {delta}"
		return message

def get_rate(result, country):
	if country=="BEL":
		return result["Cur_OfficialRate"]
	else: 
		return result[0]["rate"]

def divide_date(date, is_prev=False):
	date=date.split(".")
	day=date[0]
	month=date[1]
	year=date[2]
	if is_prev:
		day=int(day)-1
		return f"{day}.{month}.{year}"

	return day, month, year

def get_url_on_date(country, curr, date):
	if country=="BEL":
		rb_currency_for_today_url= f"https://www.nbrb.by/api/exrates/rates/{curr}?parammode=2"
		result=do_request(rb_currency_for_today_url)
		if result:
			curr_id=result["Cur_ID"]
			day, month, year=divide_date(date)
			date=f"{year}-{month}-{day}"
			url = f"https://www.nbrb.by/api/exrates/rates/{curr_id}?ondate={date}"
			return url
	elif country=="UKR":
		day, month, year=divide_date(date)
		date=f"{year}{month}{day}"
		url=f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={curr}&date={date}&json"
		return url
	else:
		print("Страны нет в списке поддерживаемых")

def changes_curr(user):
	name=user["name"]
	currency=user["currency"]
	country=user["country"]

	for curr in currency:
		message = f"Привет {name}, за последние дни динамика курса {curr}  изменилась так:"
		for day in days_ago:
			url_now=get_url_on_date(country,curr, day)
			result_now=do_request(url_now)
			
			if result_now:
				is_prev=True
				date_prev=divide_date(day, is_prev)
				url_prev=get_url_on_date(country,curr, date_prev)
				result_prev=do_request(url_prev)

				if result_prev:
					rate_date=get_rate(result_now, country)
					rate_prev=get_rate(result_prev, country)

					change_rate=round(rate_date-rate_prev, 5)

					message=add_text(day, change_rate, message)
				else:
					return
			else:
				return
		print(message)





days_ago = ["22.11.2020", "21.11.2020", "20.11.2020", "19.11.2020", "18.11.2020"]  

"""
пример - https://www.nbrb.by/api/exrates/rates/298?ondate=2020-11-25
ukr_currency_for_data_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=<АББРЕВИАТУРА ВАЛЮТЫ>&date=<ГОДМЕСЯЦЧИСЛО>&json"
пример - https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20200302&json
"""

ok_codes=(200, 201, 202)

user_bel={"name":"Belka",
			"country":"BEL",
			"currency":["USD", "EUR"]}

user_ukr={"name":"Ukrai",
			"country":"UKR",
			"currency":["USD", "EUR"]}

changes_curr(user_bel)

changes_curr(user_ukr)




