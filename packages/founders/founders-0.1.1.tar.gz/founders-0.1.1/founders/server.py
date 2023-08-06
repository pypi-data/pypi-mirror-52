import requests
import json

class server_info:
	def __init__(self, _id):
		try:
			r = requests.get('http://api.founders.gg/servers/{}'.format(_id))
			json_data = r.json()[0]

			# example: [{"domain":"founders.gg","ip":"108.79.43.45","port":25565,"name":"Founders","mRam":500,"xRam":6000,"server-jar":"spigot-1.14.4"}]
			if r.status_code == 200:
				self.success = True
				self.domain = json_data['domain']
				self.ip = json_data['ip']
				self.port = json_data['port']
				self.name = json_data['name']
				self.mRam = json_data['mRam']
				self.xRam = json_data['xRam']
				self.serverJar = json_data['server-jar']

			# example: {"error":"This resource was not found"}
			else:
				self.success = False

		except:
			self.success = False

def info(_id):
	return server_info(_id)

def all():
	return {
		'Founders': 1,
		'IAC': 2,
		'Founders 2': 3,
		'Vnlla': 4
	}