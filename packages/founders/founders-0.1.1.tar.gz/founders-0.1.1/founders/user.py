import requests
import json

class user_info:
	def __init__(self, _id):
		try:
			r = requests.get('http://api.founders.gg/users/{}'.format(_id))
			json_data = r.json()[0]

			# example: [{'username': 'Xelada', 'rank': 'Admin', 'servers': '2,4', 'lastSeen': 1568418961, 'created': 0}]
			if r.status_code == 200:
				self.success = True
				self.username = json_data['username']
				self.rank = json_data['rank']
				self.servers = json_data['servers']
				self.lastSeen = json_data['lastSeen']
				self.created = json_data['created']

			# example: {"error":"This resource was not found"}
			else:
				self.success = False
				
		except:
			self.success = False

def info(_id):
	return user_info(_id)

def all():
	return {
		'Xelada': 1,
		'dylanrocks2': 56,
		'shupik': 65,
		'Xeladarocks': 66,
		'TestUser1': 71,
		'TestUser2': 72
	}