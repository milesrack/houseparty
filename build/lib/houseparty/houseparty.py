import requests
import os
import re
from getpass import getpass
import sys
import struct
import time
from threading import Thread

if os.name == 'nt':
	PIC_DIR = os.path.join(os.environ['USERPROFILE'],'Pictures','houseparty-avatars')
else:
	PIC_DIR = os.path.join(os.environ['HOME'],'Pictures','houseparty-avatars')

class Houseparty:
	def __init__(self, username, password):
		self.user = Houseparty.login(username, password)
		if self.user:
			self.auth_token = self.user['tokenId']

	def login(username,password):
		#\x10 + len(username) + username \x12 + len(password) + password
		login_payload = struct.pack('BB',10,len(username)) + username.encode('utf-8') + struct.pack('BB',18,len(password)) + password.encode('utf-8')
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
			'Accept': 'application/x-protobuf',
			'Accept-Language': 'en-US,en;q=0.5',
			'Content-Type': 'application/x-protobuf',
			'X-Api-Version': '3',
			'X-Client-Identifier': 'com.lifeonair.houseparty',
			'X-Client-MarketingVersion': 'f457441d5a67c5f1acbaad2b3c79d0449166120f',
			'X-Client-Version': '5810',
			'X-Os-Type': 'chrome',
			'X-Os-Version': '99.0.7113.93',
			'X-Sequence-Id': '3',
			'Origin': 'https://app.houseparty.com',
			'DNT': '1',
			'Connection': 'keep-alive',
			'TE': 'Trailers'
		}
		try:
			t = requests.post('https://api2.thehousepartyapp.com/me/tokens', data=login_payload, headers=headers)
			token = t.text[2:66]
			r = requests.get('https://api2.thehousepartyapp.com/me', headers={'authorization': f'Bearer {token}'})
			data = r.json()
		except:
			return None
		else:
			return data

	def change_avatar(self,file):
		try:
			with open(file, 'rb') as f:
				image = f.read()
			headers = {'authorization': f'Bearer {self.auth_token}'}
			r = requests.put('https://api2.thehousepartyapp.com/me/avatar/raw', data=image, headers=headers)
			data = r.json()
			self.user['pfp'] = 'https://res.cloudinary.com/lifeonair/image/upload/h_1000,w_1000,dpr_1/' + self.user["user"]["avatarId"]
		except:
			return None
		else:
			return data

	def change_display_name(self,name):
		headers = {
			'authority': 'api2.thehousepartyapp.com',
			'method': 'PUT',
			'path': '/me',
			'scheme': 'https',
			'accept': 'application/x-protobuf',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9',
			'authorization': f'Bearer {self.auth_token}',
			'content-length': f'{4 + len(name)}',
			'content-type': 'application/x-protobuf',
			'dnt': '1',
			'origin': 'https://app.houseparty.com',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'cross-site',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'x-api-version': '3',
			'x-client-identifier': 'com.lifeonair.houseparty',
			'x-client-marketingversion': 'f457441d5a67c5f1acbaad2b3c79d0449166120f',
			'x-client-version': '5810',
			'x-os-type': 'chrome',
			'x-os-version': '89.0.4389.114',
			'x-sequence-id': '11',
			'x-user-session-id': '1623534469341',
		}
		data = struct.pack('BBBB',26,len(name)+2,10,len(name)) + name.encode('utf-8')
		r = requests.put('https://api2.thehousepartyapp.com/me',data=data, headers=headers)
		if r.status_code == 200:
			return True
		else:
			return None

	@staticmethod
	def check_username(username):
		r = requests.get(f'https://api2.thehousepartyapp.com/users/availability/username?value={username}')
		data = r.json()
		if len(data) == 0:
			return {'available': False, 'valid': False}
		elif data['valid']:
			return {'available': False, 'valid': True}
		elif data['valid'] and data['available']:
			return {'available': True, 'valid': True}

	def change_username(self,username):
		data = struct.pack('BBBB',18,len(username)+2,10,len(username)) + username.encode('utf-8')
		headers = {
			'authority': 'api2.thehousepartyapp.com',
			'method': 'PUT',
			'path': '/me',
			'scheme': 'https',
			'accept': 'application/x-protobuf',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9',
			'authorization': f'Bearer {self.auth_token}',
			'content-length': '10',
			'content-type': 'application/x-protobuf',
			'dnt': '1',
			'origin': 'https://app.houseparty.com',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'cross-site',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'x-api-version': '3',
			'x-client-identifier': 'com.lifeonair.houseparty',
			'x-client-marketingversion': 'f457441d5a67c5f1acbaad2b3c79d0449166120f',
			'x-client-version': '5810',
			'x-os-type': 'chrome',
			'x-os-version': '89.0.4389.114',
			'x-sequence-id': '18',
			'x-user-session-id': '1623540377394',
		}
		r = requests.put('https://api2.thehousepartyapp.com/me', data=data, headers=headers)
		if r.status_code == 200:
			return True
		else:
			return None

	def in_house_alert(self):
		headers = {'authorization': f'Bearer {self.auth_token}'}
		r = requests.post('https://api2.thehousepartyapp.com/me/in_the_house', headers=headers)
		if r.status_code == 200:
			return True
		else:
			return None

	def online_friends(self):
		headers = {'authorization': f'Bearer {self.auth_token}'}
		r = requests.get('https://api2.thehousepartyapp.com/me/presence', headers=headers)
		return r.json()

	def relationships(self):
		headers = {'authorization': f'Bearer {self.auth_token}'}
		r = requests.get('https://api2.thehousepartyapp.com/me/relationships', headers=headers)
		return r.json()

	def suggestions(self):
		headers = {'authorization': f'Bearer {self.auth_token}'}
		r = requests.put('https://api2.thehousepartyapp.com/me/suggestions', headers=headers)
		return r.json()

	def search(self,text):
		if len(text) < 3:
			return False
		headers = {'authorization': f'Bearer {self.auth_token}'}
		r = requests.get('https://api2.thehousepartyapp.com/users/search', params={'query': text}, headers=headers)
		return r.json()


class User:
	def __init__(self, auth_token, username):
		self.uid = User.get_uid(username)
		self.auth_token = auth_token
		if self.uid:
			self.user = User.get_user_info(self)

	@staticmethod
	def get_uid(username):
		try:
			r = requests.get(f'https://houseparty.com/add/{username}')
			uid = re.findall(r'friend_id: "(.*)"', r.text)[0]
			return uid
		except:
			return None

	def get_user_info(self):
		headers = {'authorization': f'Bearer {self.auth_token}'}
		r = requests.get(f'https://api2.thehousepartyapp.com/me/relationships/{self.uid}', headers=headers)
		data = r.json()
		return data

	def get_avatar(self,output_dir=PIC_DIR,size=1000):
		avatar_url = f'https://res.cloudinary.com/lifeonair/image/upload/h_{size},w_{size},dpr_1/{self.user["avatarId"]}'
		try:
			pic_data = requests.get(avatar_url).content
			if not os.path.exists(PIC_DIR):
				os.mkdir(PIC_DIR)
			filepath = os.path.join(PIC_DIR,self.uid+'.jpg')
			with open(filepath, 'wb') as avatar:
				avatar.write(pic_data)
		except:
			return None
		else:
			return True

	def say_hi(self,amount=1):
		headers = {'authorization': f'Bearer {self.auth_token}'}
		for i in range(amount):	
			r = requests.post(f'https://api2.thehousepartyapp.com/users/{self.uid}/greet', headers=headers)
			if r.status_code == 200:
				continue
			else:
				return None
		return True

	def ring(self,amount=1):
		headers = {
			'authority': 'api2.thehousepartyapp.com',
			'method': 'POST',
			'path': f'/users/{self.uid}/start_call',
			'scheme': 'https',
			'accept': 'application/x-protobuf',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9',
			'authorization': f'Bearer {self.auth_token}',
			'content-length': '0',
			'content-type': 'application/x-protobuf',
			'dnt': '1',
			'origin': 'https://app.houseparty.com',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'cross-site',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'x-api-version': '3',
			'x-client-identifier': 'com.lifeonair.houseparty',
			'x-client-marketingversion': 'f457441d5a67c5f1acbaad2b3c79d0449166120f',
			'x-client-version': '5810',
			'x-os-type': 'chrome',
			'x-os-version': '89.0.4389.114',
			'x-sequence-id': '95',
		}
		for i in range(amount):
			r = requests.post(f'https://api2.thehousepartyapp.com/users/{self.uid}/start_call', headers=headers)
			if r.status_code == 200:
				continue
			else:
				return None
		return True

	def send_message(self,message, amount=1):
		data = struct.pack('B',24) + self.uid.encode('utf-8') + struct.pack('BB',18,len(message)) + message.encode('utf-8')
		headers = {
			'authority': 'api2.thehousepartyapp.com',
			'method': 'POST',
			'path': '/notes/send',
			'scheme': 'https',
			'accept': 'application/x-protobuf',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9',
			'authorization': f'Bearer {self.auth_token}',
			'content-length': f'{len(data) + 1}',
			'content-type': 'application/x-protobuf',
			'dnt': '1',
			'origin': 'https://app.houseparty.com',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'cross-site',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'x-api-version': '3',
			'x-client-identifier': 'com.lifeonair.houseparty',
			'x-client-marketingversion': 'f457441d5a67c5f1acbaad2b3c79d0449166120f',
			'x-client-version': '5810',
			'x-os-type': 'chrome',
			'x-os-version': '89.0.4389.114',
			'x-sequence-id': '21',
			'x-user-session-id': '1623536787282',
		}
		for i in range(amount):
			r = requests.post('https://api2.thehousepartyapp.com/notes/send', data=data, headers=headers)
			if r.status_code == 200:
				continue
			else:
				return None
		return True
