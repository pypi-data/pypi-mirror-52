import requests

class xrptipbot:
	def __init__(self, token):
		self.token = token
		self.baseUrl = "https://www.xrptipbot.com/app/api"

	def login(self, platform, model):
		url = self.baseUrl + "/action:login/"
		payload = {
			"token":self.token,
			"platform":platform,
			"model":model
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def unlink(self):
		url = self.baseUrl + "/action:unlink/"
		payload = {
			"token":self.token
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def get_balance(self):
		url = self.baseUrl + "/action:balance/"
		payload = {
			"token":self.token
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def tip(self, amount, to, existingDestination):
		url = self.baseUrl + "/action:tip/"
		payload = {
			"token":self.token,
			"amount":amount,
			"to":to,
			"existingDestination":existingDestination
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def get_stats(self):
		url = self.baseUrl + "/action:userinfo/"
		payload = {
			"token":self.token
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def get_contacts(self):
		url = self.baseUrl + "/action:contacts/"
		payload = {
			"token":self.token
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def lookup_user(self, query):
		url = self.baseUrl + "/action:lookup/"
		payload = {
			"token":self.token,
			"query":query
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def create_paper_wallet(self, note):
		url = self.baseUrl + "/action:paper-proposal/"
		payload = {
			"token":self.token,
			"note":note
		}
		r = requests.post(url=url, data=payload)
		return r.content

	def bump(self, amount, aps=None, geo=None, nfc=None):
		url = self.baseUrl + "/action:bump/"
		payload = {
			"token":self.token,
			"amount":amount,
			"aps":aps,
			"geo":geo,
			"nfc":nfc
		}
		r = requests.post(url=url, data=payload)
		return r.content		

