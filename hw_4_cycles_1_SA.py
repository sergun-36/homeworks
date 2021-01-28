songs = [
		{"artist":"Disturbed", "name": "The light" ,"long": 4.16, "band": True, "album":"Immortalized"},
		{"artist":"Guns N' Roses", "name": "Civil War", "long": 7.42, "band":True, "album": "Use Your Illusion II"},
		{"artist":"Ben Nichols", "name": "The last pale light in the west", "long": 3.24, "band":False},
		{"artist":"Lumen", "name":"Burn", "band":True},
		{"artist":"Машина времени", "name":"Синяя птица", "long":3.42},
		{"long":3.47, "band":True, "album":"Fight club"},
		{}
		]

atributes=["name","artist", "long", "band", "album"]

if songs:
	for song in songs:
		if song:
			for atribut in atributes:
				if atribut not in song.keys():
					song[atribut]=None
					if ("name" in song.keys()) and song["name"]:
						print(f"У песни с названием \"{song['name']}\" отсутствуeт полe: {atribut}")
					elif "artist" in  song.keys() and song["artist"]:
						print(f"У песни исполнителя \"{song['artist']}\" отсутствует поле {atribut}")
					else:
						print(f"У той самой песни, ,без названия и исполнителя, отсутствуeт поле: {atribut}")
		else:
			print("В списке песен пустой словарью Пожалуйста проверьте заполнение")
else:
	print("Your songs list is empty")