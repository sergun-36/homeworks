#Задание 1
weather_info =  {"18.10.2020": {"weather": "Туман"},
				 "19.10.2020": {"weather": "Дождь"},
				 "20.10.2020": {"weather": "Ливень"},
				 "21.10.2020" :{"weather": "Солнечно"}}

date="20.10.2020"

message="Сегодня {0} : {1}".format(date, weather_info[date]["weather"])
print(message)




#ЗАДАНИЕ 2
weather_info = {
				"18.10.2020": {"weather": {"temp": 25, "weather_type": "Ливень"}},
  				"19.10.2020": {"weather": {"temp": 17, "weather_type": "Солнечно"}},
				"20.10.2020": {"weather": {"temp": 21, "weather_type": "Туман"}},
				"21.10.2020": {"weather": {"temp": 12, "weather_type": "Ветренно"}}
				}
date="21.10.2020"

message="Сегодня {0}. При {1} градусах - {2}".format(date, weather_info[date]["weather"]["temp"], weather_info[date]["weather"]["weather_type"])
print(message)


#ЗАдание 3

#date="any date"# for check
#weather_info={}#для проверки
date="19.10.2020"
if len(weather_info)>0 :
		if date in weather_info:
			message="Сегодня {0}. При {1} градусах - {2}".format(date, weather_info[date]["weather"]["temp"], weather_info[date]["weather"]["weather_type"])
			print("После всех проверок", message)
		else:
			print("нет такого ключа")
else:
	print("Dict is empty")