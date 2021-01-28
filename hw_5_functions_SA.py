import requests
import datetime # для получения даты сегодня и периода для динамики

def get_dates_from_message(message):
	print("check")
	message=message.upper()		
	if message.find("ДАТУ")>=0:
		words_message=message.split(" ")
		index_date=words_message.index("ДАТУ")+1
		date=words_message[index_date]
		dates=date.split(".")
		dates.reverse()
		dates="-".join(dates)
		return [dates]
	if message.find("СЕГОДНЯ")>=0:
		dates=str(datetime.date.today())
		return [dates]
	if message.find("ДИНАМИКА")>=0:
		words_message=message.split(" ")
		index_days_ago=words_message.index("ДНЕЙ")-1
		days_ago=int(words_message[index_days_ago])
		dates=[]
		for i in range(0, days_ago+1):
			dates.append(str((datetime.datetime.now()-datetime.timedelta(days=i)).date()))
		return dates	


def get_curr_from_message(message):
	message=message.upper()	
	if message.find("ДЛЯ")>=0:
		currs=message.split("ДЛЯ ")[1]
		currs=currs.split(",")
		currencys=[]
		for curr in currs:
			#удаляем пробельные символы в конце и начале строки
			currencys.append(curr.strip(" "))
			
		#удаляем многоточие или другие знаки перпинания с последней абрревиатуры
		# Состоит ли строка из букв		
		while not currencys[len(currencys)-1].isalpha():
			currencys[len(currencys)-1]=currencys[len(currencys)-1][:-1]
				
		return currencys


def get_data_for_answer(message):
	message=message.upper()	
	"""
	types_request={"dinamika":"Привет {}, за последние дни динамика курса {}  изменилась так:",
					"rate_on_date":"Курс {} на дату {} составляет ",
					"rate_on_today":"курс {} на сегодня {} составляет: "}
	"""				

	currencys=get_curr_from_message(message)
	if not currencys:
		print("Впишите интересющие вас валюты в конце запроса после слова ДЛЯ")
		return
	dates=get_dates_from_message(message)
	if not dates:
		print("не найдены даты ")
		return

	if message.find("ДИНАМИКА")>=0:
		return {"type":"dinamika",
				"text_model":"\nЗа последние дни динамика курса {} {} по отношению к  {} изменилась так:",
				"currencys":currencys,
				"dates": dates}
	if message.find("ДАТУ")>=0:
		return {"type":"rate_on_date",
				"text_model":"\nКурс {} на дату {} составляет ",
				"currencys":currencys,
				"dates": dates}
	if message.find("СЕГОДНЯ")>=0:
		return {"type":"rate_on_today",
				"text_model":"\nкурс {} {} на сегодня составляет: ",
				"currencys":currencys,
				"dates": dates}


def do_request(url):
	ok_codes=(200, 201, 202)
	response=requests.get(url)
	if response.status_code in ok_codes:
		result=response.json()
		return result
	else:
		print(f"Запрос вернул ошибку со статусом {response.status_code}")


def get_curr_scale(result, country):
	if country=="UKR":
		return 1
	if country=="BY":
		curr_scale=result["Cur_Scale"]
		return curr_scale


def get_local_curr(country):
	if country=="UKR":
		return "украинская гривна"
	if country=="BY":
		return "белорусский рубль"


def add_text(changes_rates, message):
	for date in changes_rates:
		delta=changes_rates[date]
		if delta >0:
			message+=f"\n{date}: +{delta}"
		else:
			message+=f"\n{date}: {delta}"
	return message


def get_rate(result, country):
	if country=="BY":
		return result["Cur_OfficialRate"]
	else: 
		return result[0]["rate"]


def format_date(date, country):
	if country=="BY":
		return date
	if country=="UKR":
		date="".join(date.split("-"))
		return date


def get_url_on_date(country, curr, date):
	date=format_date(date, country)
	if country=="BY":
		rb_currency_for_today_url= f"https://www.nbrb.by/api/exrates/rates/{curr}?parammode=2"
		result=do_request(rb_currency_for_today_url)
		if result:
			curr_id=result["Cur_ID"]
			url = f"https://www.nbrb.by/api/exrates/rates/{curr_id}?ondate={date}"
			return url
	if country=="UKR":
		url=f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={curr}&date={date}&json"
		return url


def curr_data_on_date(country, curr, date):
	url=get_url_on_date(country, curr, date)
	if not url:
		return
	result=do_request(url)
	if not result:
		if not type(result)==None:
			print(f"Такой валюты как {curr} не существует")
		return
	rate=get_rate(result, country)
	scale=get_curr_scale(result, country)
	return {"rate":rate,
			"scale":scale}


def get_rates_on_date(country, datas_for_answer):
	currencys=datas_for_answer["currencys"]
	text_model=datas_for_answer["text_model"]
	dates=datas_for_answer["dates"]
	text_answer=""
	local_curr=get_local_curr(country)
	for date in dates:
		for curr in currencys:
			curr_data=curr_data_on_date(country, curr, date)
			if curr_data:
				rate=curr_data["rate"]
				scale=curr_data["scale"]
				text_answer+=text_model.format(curr, date)
				text_answer+=f"{rate} {local_curr} за {scale} {curr}"
	return text_answer


def get_changes_rates(country, datas_for_answer):
	currencys=datas_for_answer["currencys"]
	text_model=datas_for_answer["text_model"]
	text_answer=""
	dates=datas_for_answer["dates"]
	local_curr=get_local_curr(country)
	text_delta=""
	for curr in currencys:
		scale=""
		rates=[]
		for date in dates:
			curr_datas=curr_data_on_date(country, curr, date)
			if curr_datas:
				scale=curr_datas["scale"]
				rate=curr_datas["rate"]
				rates.append(rate)
			else:
				break
		else:
			text_delta+=text_model.format(scale, curr, local_curr)
			changes_rates={}
			for i in range(0, len(dates)-1):
				changes_rates[dates[i]]=round(rates[i]-rates[i+1], 5)	
				#message=add_text(day, change_rate, message)
			text_delta=add_text(changes_rates, text_delta)
			text_answer=text_delta


	return text_answer


def get_rates_on_today(country, datas_for_answer):
	currencys=datas_for_answer["currencys"]
	text_model=datas_for_answer["text_model"]
	text_answer=""
	dates=datas_for_answer["dates"]
	local_curr=get_local_curr(country)
	for date in dates:
		for curr in currencys:
			curr_data=curr_data_on_date(country, curr, date)
			if curr_data:
				rate=curr_data["rate"]
				scale=curr_data["scale"]
				text_answer+=text_model.format(scale, curr)
				text_answer+=f" {rate} {local_curr}"
	return text_answer



def handling_user_request(user, user_message):
	countrys=("BY", "UKR")
	message=user_message["message_text"]
	name=user["username"]
	country=user["country"]
	hello=f"Привет, {name}"
	if country not in countrys:
		print("Вашей станы нет в списке поддерживаемых")
		return
	datas=get_data_for_answer(message)
	if not datas:
		print("Для запроса не хватает данных")
		return
	type_request=datas["type"]
	text_model=datas["text_model"]
	if type_request=="dinamika":
		text_answer=get_changes_rates(country, datas)
		if not text_answer:
			return
		return hello+text_answer
	if type_request=="rate_on_today":
		text_answer=get_rates_on_today(country, datas)
		return hello+text_answer
	if type_request=="rate_on_date":
		text_answer=get_rates_on_date(country, datas)
		return hello+text_answer


#S.find(str, [start],[end])

user_UKR = {"username": "Taras Bulba",
		"country": "UKR"}

user_BY={"username": "Belka",
		"country":"BY"}



user=user_BY

user_message_dinamika = {"user": user,
				"message_text": "динамика курса валют за 5 дней для USD, EUR, RUB, Gypd.",
				"current_date":"25.11.2020"}


user_message_today = {"user": user,
				"message_text": "Курсы  валют на сегодня  для USD, EUR, RUB, Gypr",
				"current_date":"25.11.2020"}


user_message_on_date= {"user": user,
				"message_text": "курсы валют на дату 21.11.2020 для USD, EUR, RUB, Cypd",
				"current_date":"25.11.2020"}

user_message=user_message_dinamika

print(handling_user_request(user, user_message))

