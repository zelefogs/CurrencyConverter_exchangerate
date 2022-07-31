import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import re
import datetime


def available_currencies():
	"""
	:return: dict with available currencies to convert
	"""
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
	"""
	Displays a list of currencies with description
	:param d_cur: dict of available currencies
	:return:
	"""
	for k, v in d_cur['symbols'].items():
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
	A function that returns how much the euro cost in currency on a historical date
	:param currency: for example USD
	:param date: for example 20-13-1999
	:param need_prnt: func print string if True
	:return: currency to euro ratio
	"""
	if currency in available_currencies()['symbols']:
		date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
		url = f'https://api.exchangerate.host/{str(date.year)}-{str(date.month + 1)}-{str(date.day)}'
		params = {'symbols': currency}
		data = validate_request(url, params)
		if data[0]:
			rates = data[1]['rates']
			if need_prnt:
				print(f'{date} 1 EUR cost {round(list(rates.items())[0][1], 2)} {list(rates.items())[0][0]}')
			return rates.get(currency)


def time_series_data(start_date: str, end_date: str, currency: str, base="EUR"):
	"""
	Takes start_date, end_date as input and returns a dictionary with keys:date,values: rate currency to base
	:param start_date: in format month-day-year
	:param end_date:   in format month-day-year
	:param currency:   available currencies can be obtained using the function available_currencies()
	:param base:
	:return:           dictionary with keys:date,values: rate currency to base, currency and base for draw graph
	"""
	start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
	end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y").date()
	if start_date > end_date:
		return 'start_date must be less than end_date'
	params = {'start_date': str(start_date), 'end_date': str(end_date), 'symbols': currency, 'base': base}
	url = 'https://api.exchangerate.host/timeseries/'
	data = validate_request(url, params)
	if data[0]:
		if currency not in data[1]['rates'].get(str(start_date)).keys():
			return 'There is no information about this currency'
		return data[1]['rates'], currency, base


def view_graph(dict_rates, currency, base):
	"""
	Function draws a graph using matplotlib axis x - date, axis y - currency rate to base
	Parameters can be passed like this *time_series_data('30-05-2021', '30-05-2022', 'USD', 'EUR')
	:param dict_rates:
	:param currency:
	:param base:
	:return:
	"""
	xdata = [datetime.datetime.strptime(item, '%Y-%m-%d') for item in dict_rates.keys()]
	ydata = [item.get(currency) for item in dict_rates.values()]
	fig, ax = plt.subplots()
	ax.plot(xdata, ydata)
	ax.set(xlabel='date', ylabel=f'{currency}',
	       title=f'{base} to {currency} ratio in {xdata[0].year}/{xdata[0].month}-{xdata[-1].year}/{xdata[-1].month}')
	ax.grid()
	locator = mdates.MonthLocator()
	ax.xaxis.set_major_locator(locator)
	fig.set_figwidth(12)
	plt.gcf().autofmt_xdate()
	fig.savefig("graph.png")
	plt.show()


def validate_request(url, params=None):
	response = requests.get(url, params=params)
	if response.status_code == requests.codes.ok:
		data = response.json()
		if data['success']:
			return True, data


#view_graph(*time_series_data('30-05-2021', '30-05-2022', 'RUB', 'USD'))
# print(convert_currency("200 USD to RUB", True))
# print(historical_rates('RUB','30-05-2010', False))
# print(get_available(available_currencies()))
