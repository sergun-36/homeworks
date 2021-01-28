#задание 2

user_one={"name":"Sergei",
		"my_songs":{}}
print(user_one)

songs=[{"artist":"Evanescence", "name":"Bring me to life"},
		{"artist":"Evanescence", "name":"Hello"},
		{"artist":"Nirvana", "name":"Smells like teen spirit"},
		{"artist":"Evanescence","name":"Lithium"},
		{"artist":"Evanescence","name":"My Immortal"},
		{"artist":"Nirvana", "name":"Come as you are"},
		{"artist":"Linkin Park", "name":"In the end"},
		{"artist":"Linkin Park","name":"New divide"},
		{"artist":"Keiino","name":"Spirit in the sky"},
		{"artist":"Linkin Park", "name":"From the inside"},
		{"artist":"Nirvana", "name":"Smells like teen spirit"},
		{"name":"Gimn"},
		{"name":"Ballada"},
		]
user=user_one

if songs:
	for song in songs:
		if song:
			if "artist" not in song.keys():
				song["artist"]=None
			if "name" not in song.keys():
				song["name"]=None
			if song["artist"] not in user["my_songs"].keys():
				if song["artist"]:
					print(f"Добавляем нового исполнителя \"{song['artist']}\" ")
					user["my_songs"][song["artist"]]=[song["name"]]
				else:
					print(f"Добавляем каталог для  песен с неизвестным или  без исполнителя")
					user["my_songs"][song["artist"]]=[song["name"]]
			else:
				print(f"\"{song['artist']}\" уже существует")
				if song["name"] not in user["my_songs"][song["artist"]]:
					user["my_songs"][song["artist"]].append(song["name"])
					user["my_songs"][song["artist"]]=sorted(user["my_songs"][song["artist"]])

				else:
					print(f"Песня \"{song['name']}\" уже есть в списке")

		else:
			print("Вместо песни пустой dict")
else:
	print("Songs list is empty")

print(user_one)

#Задание 3 Совпадение вкусов
print("ЗАДАНИЕ 3. Совпадение вкусов по наличию общих песен")

user_two={"name":"Valeri",
			"my_songs":{"Evanescence":["Bring me to life", "Hello", "Lithium"]}}

profile_one=user_one
profile_two=user_two
songs_count=0
same_songs=0


if profile_one:
	if profile_two:
		for singer in profile_one["my_songs"]:
			for song in (profile_one["my_songs"][singer]):
				songs_count+=1
				if singer in profile_two["my_songs"]:
					if song in profile_two["my_songs"][singer]:
						#print("есть такая песня")
						same_songs+=1
		print(f"Уровень совпадения вкуса у пользователя {profile_one['name']} с пользователем {profile_two['name']} составляет {(same_songs/songs_count)*100:.2f} процентов")

	else:
		print("Контрольный профиль пуст")	
else:
	print("Сравниваемый профиль пуст")