#SHA256 Password Cracking project from Riley Kidd 247CTF

#We will use pwntool and sys modules

from pwn import *
import sys

#We will use parameters from the command line.

if len(sys.argv) !=2:
	print("Invalid Arguments!")
	print(">> {} <sha256sum>".format(sys.argv[0]))
	exit()

#The first parameter will be assigned to wanted_hash
wanted_hash = sys.argv[1]

#Assigning a passwordfile
password_file = "rockyou.txt"
attempts = 0

with log.progress("Attempting to crack: {}!\n".format(wanted_hash)) as p:
	with open(password_file, "r", encoding='latin-1') as password_list:
		for password in password_list:
			password = password.strip("\n").encode('latin-1')
			password_hash = sha256sumhex(password)
			p.status("[{}] {} == {}".format(attempts, password.decode('latin-1'), password_hash))
			if password_hash == wanted_hash:
				p.success("Password has found after {} attempts! {} hashes to {}!".format(attempts, password.decode('latin-1'), password_hash))
				exit()
			attempts += 1
		p.failure("Password hash not found!")
