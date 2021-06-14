from houseparty import Houseparty, User

def rotate_names(*argv):
	while True:
		for name in argv:
			me.change_display_name(name)
			time.sleep(2)

def rotate_avatar(*argv):
	while True:
		for picture in argv:
			me.change_avatar(picture)
			time.sleep(5)

def spam_in_house_alert():
	while True:
		me.in_house_alert()
		time.sleep(1)		

me = Houseparty('USERNAME','PASSWORD')
print(me.user)

print(me.check_username('somerandomuser123'))

me.change_avatar('C:\\Path\\to\\avatar\\image.png')
me.change_display_name(' ')
me.change_username('somerandomuser123')
me.in_house_alert()

online = me.online_friends()
print(online)

relationships = me.relationships()
print(relationships)

suggestions = me.suggestions()
print(relationships)

search = me.search('tom')
print(search)

friend = User(me.auth_token,'USERNAME')
print(friend.user)

friend.get_avatar()
friend.say_hi()
friend.ring()
friend.send_message('hello!') # Not functional yet


# Continuously rotate display names, avatar images, and spam in house alerts
try:
	rotate_names = Thread(target=rotate_names, args=('name_1','name_2','name_3'))
	rotate_names.daemon=True
	rotate_names.start()

	rotate_avatar = Thread(target=rotate_avatar, args=('C:\\Path\\to\\avatar\\image1.png','C:\\Path\\to\\avatar\\image2.png','C:\\Path\\to\\avatar\\image3.png'))
	rotate_avatar.daemon=True
	rotate_avatar.start()

	spam_in_house_alert = Thread(target=spam_in_house_alert)
	spam_in_house_alert.daemon=True
	spam_in_house_alert.start()

	while True:
		time.sleep(100)
except (KeyboardInterrupt, SystemExit):
	sys.exit()
