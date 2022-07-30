import requests
import pprint


def available_currencies():
	url = 'https://api.exchangerate.host/symbols'
	response = requests.get(url)
	if response.status_code==requests.codes.ok:
		data = response.json()
		if 'success' in data:
			for k,v in data['symbols'].items():
				if 'code' in v:
					v.pop('code')
			return data['symbols']
	return 'Connection error'


def get_available(d_cur):
	'''
	Displays a list of currencies with description
	:param d_cur: dict of available currencies
	:return:
	'''
	for k,v in d_cur.items():
		print(k, *v.values())


get_available(available_currencies())

