name="Sergei"
date="21.05.2020"

currency_name="USd"
currency_scale=1
currency_rate=2.6

if currency_scale>1:
	currency_rate=currency_rate/currency_scale



currency_message="hello {0}. Today {1}. Currency rate: one {2} equals {3} BYN"
currency_message_usd=currency_message.format(name, date, currency_name.upper(), currency_rate)

print(currency_message_usd)

currency_name="Rub"
currency_rate=3.33
currency_scale=100

if currency_scale>1:
	currency_rate=currency_rate/currency_scale


currency_message_rub=currency_message.format(name, date, currency_name.upper(), currency_rate)

print(currency_message_rub)

currency_message=F"hello {name}. Today {date}. Currency rate: one {currency_name} equals {currency_rate} BYN"
print(currency_message)