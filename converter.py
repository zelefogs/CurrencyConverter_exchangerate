import requests
import re
import datetime
import pprint


def available_currencies():
	url = 'https://api.exchangerate.host/symbols'
	vldt = validate_request(url)
	if vldt[0]:
		data = vldt[1]
		for k, v in data['symbols'].items():
			if 'code' in v:
				v.pop('code')
		return data
	else:
		return 'Connection error'


def get_available(d_cur):
	'''
	Displays a list of currencies with description
	:param d_cur: dict of available currencies
	:return:
	'''
	for k,v in d_cur.items():
		print(k, *v.values())


def convert_currency(val_from_to: str, need_prnt=False):
	"""
	:param val_from_to: example: "1 USD to EUR"
	:param need_prnt: func print string if True
	:return: converted number (float)
	"""
	pattern = r'[\d]*\.?\d* \w* to \w*'
	vldt_input = re.search(pattern, val_from_to).group()
	if vldt_input:
		dict_currencies = available_currencies()['symbols']
		amount = float(vldt_input.split()[0])
		from_cur = vldt_input.split()[1].upper()
		to_cur = vldt_input.split()[3].upper()
		if from_cur and to_cur in dict_currencies:
			params = {'from': from_cur, 'to': to_cur, 'amount': amount}
			url = f'https://api.exchangerate.host/convert/'
			vldt = validate_request(url, params)
			if vldt[0]:
				data = vldt[1]
				converted_amount = data.get('result')
				converted_amount = round(converted_amount, 2)
				if need_print:
					print(f'{amount} {from_cur} = {converted_amount} {to_cur}')
				return converted_amount
		return 'Invalid currencies'
	return 'Invalid input'


def historical_rates(currency: str, date: str, need_prnt=False):
	"""

	:param currency: for example USD
	:param date: for example 20-13-1999
	:param need_prnt: func print string if True
	:return: currency to euro ratio
	"""
	if currency in available_currencies()['symbols']:
		date = datetime.datetime.strptime(date,"%d-%m-%Y").date()
		url = f'https://api.exchangerate.host/{str(date.year)}-{str(date.month+1)}-{str(date.day)}'
		params = {'symbols': currency}
		data = validate_request(url, params)
		if data[0]:
			rates = data[1]['rates']
			if need_prnt:
				print(f'{date} 1 EUR cost {round(list(rates.items())[0][1], 2)} {list(rates.items())[0][0]}')
			return rates.get(currency)


def validate_request(url, params=None):
	response = requests.get(url, params=params)
	if response.status_code==requests.codes.ok:
		data = response.json()
		if 'success' in data:
			return True, data



#print(convert_currency("200 USD to RUB", True))
#print(historical_rates('RUB','30-05-2010', False))
#get_available(available_currencies())