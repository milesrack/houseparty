# houseparty
## Description
A python package to interact with Houseparty's API. The following tasks can be automated through the use of this package:
- Logging in
- Waving
- Calling
- Messaging (not functional at the moment)
- In house alerts
- Changing profile picture
- Changing display name
- Changing username
- Checking username availability
- Viewing online friends
- Viewing relationships
- Viewing friend suggestions
- Searching for users
- Downloading a user's avatar
- Viewing account details:
	- Account ID
	- Username
	- Full name
	- Avatar ID
	- Account creation date
	- Last account update date
	- Relationship status
	- Last interaction

## Requirements
This package relies on the `requests` library. You can install it with `pip3 install requests`.

## Installation
```
pip3 install houseparty
```

## Getting started
```python
from houseparty import Houseparty, User

me = Houseparty('USERNAME','PASSWORD') # Replace this with your houseparty username and password
print(me.user) # Print your user information

friend = User(me.auth_token,'USERNAME') # Initializes an instance of a user we want to interact with, the auth token is needed to retrieve a friend's information and preform user actions (wave, ring, etc.)
print(friend.user) # Print the user's information
```
See [example.py](https://github.com/milesrack/houseparty/blob/master/example.py) for more usage examples of this package.

## Function explanations
|Function Name|Function Explanation|Number of arguments|Argument Details|Return value|
|-------------|--------------------|-------------------|----------------|------------|
|`Houseparty.login()`|Logs in a user to get an authentication token. **Called by default when initializing `Houseparty` instance.**|2|`self, username, password`: `username` and `password` must be valid Houseparty credentials.|Dictionary containing user information.|
|`Houseparty.change_avatar()`|Changes the avatar of the current user.|1|`self, file`: `file` must be a valid file path.|Dictionary containing response from avatar PUT request.|
|`Houseparty.change_display_name()`|Changes the display name of the current user.|1|`self, name`|`True` if the change was sucessful, otherwise returns `None`.|
|`Houseparty.check_username()`|Checks the availability and validity of a username.|1|`username`|Dictionary containing the validity and availibility status.|
|`Houseparty.change_username()`|Changes the username of the current user.|1|`self, username`: `username` must be available and valid.|`True` if the change was sucessful, otherwise returns `None`.|
|`Houseparty.in_house_alert()`|Sends out a **\<name> is in the house** alert.|0|`self`|`True` if the request was sucessful, otherwise returns `None`.|
|`Houseparty.online_friends()`|Returns the online friend list of the current user.|0|`self`|Dictionary containing online friends and their user details.|
|`Houseparty.relationships()`|Returns the friend list of the current user.|0|`self`|Dictionary containing all friends and their user details.|
|`Houseparty.suggestions()`|Returns friend suggestions for the current user.|0|`self`|Dictionary containing frined suggestions and their user details.|
|`Houseparty.search()`|Searches for Houseparty users.|1|`self, text`: `text` must be at least 3 characters|Dictionary of users matching the search text and their user details.|
|`User.get_uid()`|Returns the user ID of a username. **Called by default when initializing `User` instance.**|1|`username`: `username` must be a Houseparty user.|`uid` string if sucessful, otherwise returns `None`.|
|`User.get_user_info()`|Returns the user details for a `User` instance.|0|`self`|Dictionary containing user details.|
|`User.get_avatar()`|Downloads the avatar for a `User` instance.|2 (optional)|`self, output_dir, size`: `output_dir` must be a valid file path, by default it is `HOME_DIRECTORY/Pictures/houseparty-avatars`. `size` must be an integer, by default it is `1000`.|`True` if sucessful, otherwise returns `None`.|
|`User.say_hi()`|Sends a wave to the current `User` instance.|1 (optional)|`self, amount`: `amount` must be a positive integer.|`True` if sucessful, otherwise returns `None`.|
|`User.ring()`|Sendsd a call to the current `User` instance.|1 (optional)|`self, amount`: `amount` must be a positive integer.|`True` if sucessful, otherwise returns `None`.|
|`User.send_message()`|Sends a message to the current `User` instance. **Still under development and not functional at the moment.**|2 (second argument is optional)|`self, message, amount`: `amount` must be a positive integer.|`True` if sucessful, otherwise returns `None`.|
