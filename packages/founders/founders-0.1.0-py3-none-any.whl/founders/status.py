import requests
import json

class status_info:
	def __init__(self, _id):
		try:
			r = requests.get('http://api.founders.gg/status/{}'.format(_id))
			json_data = r.json()

			# example: {"Success":{"host":"108.79.43.45","port":25567}}
			if r.status_code == 200:
				json_data = json_data['Success']

				self.success = True
				self.status = True
				self.ip = json_data['host']
				self.port = json_data['port']

			# example: {"error":{"errno":"ECONNREFUSED","code":"ECONNREFUSED","syscall":"connect","address":"108.79.43.45","port":25566}}
			elif r.status_code == 500:
				json_data = json_data['error']

				self.success = True
				self.status = False
				self.ip = json_data['address']
				self.port = json_data['port']

			# example: {"error":"This resource was not found"}
			else:
				self.success = False

		except:
			self.success = False

def stat(_id):
	return status_info(_id)