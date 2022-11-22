from tkinter import *
from tkinter import ttk
import socket
import sys
import time
import os
import logging
import threading
import time
from winsound import *
from tkinter import messagebox

s=socket.socket()

def read_message(incomming_message):
	try : 
		name, message_content = incomming_message.split('#-#')
		name = name[:-1]
		message_content = message_content[:-1]
		message_content = message_content[2:]
		global readed_message
		readed_message = f"{name} : {message_content}"
	except Exception as error:
		messagebox.showerror("Erreur.","Une erreur est survenue: le message n'a pas une forme normale. Impossible à traiter!")
		


def playsound():
    return PlaySound("sound.wav", SND_FILENAME)
liste_messages = ["","","",""]
def refresh():
	try :
		while 1:
			incomming_message = s.recv(1024).decode('utf-8')
			read_message(incomming_message)
			liste_messages.append(readed_message)
			label1.configure(text = liste_messages[-4])
			label1.grid(row= 2, column = 2 )
			label2.configure(text = liste_messages[-3])
			label4.grid(row= 3, column = 2 )
			label3.configure(text = liste_messages[-2])
			label4.grid(row= 4, column = 2 )
			label4.configure(text = liste_messages[-1])
			label4.grid(row= 5, column = 2 )
			playsound()
	except ConnectionResetError:
		InfoLabel.configure(text= "Connexion au serveur perdue.", fg = 'red')
		InfoLabel.grid(padx = 60, row= 0, column = 2 )

def envoyer_un_message():
	message = message_a_envoyer.get()
	message = message.encode()
	s.send(message)
	message_entry.delete(0, END)

def login_verify():
	try : 
		serverport_1 = int(serverport.get())
		servername_1 = servername.get()
		s.connect((servername_1,serverport_1))
		screen1 = Toplevel(screen)
		screen1.geometry("300x250")
		screen1.title("Projet Y - Chat")
		mainContainer = Frame(screen1)
		global InfoLabel
		InfoLabel = Label(mainContainer, text = 'Connected to Chat.', fg = 'green', font = ("Calibri", 11))
		InfoLabel.grid(padx = 100, row= 0, column = 2 )
		global label1
		label1 = Label(mainContainer, text="")
		label1.configure(text="Waiting for a message...")
		label1.grid(row= 2, column = 2 )
		global label2
		label2 = Label(mainContainer, text="")
		label2.configure(text="Waiting for a message...")
		label2.grid(row= 3, column = 2 )
		global label3
		label3 = Label(mainContainer, text="")
		label3.configure(text="Waiting for a message...")
		label3.grid(row= 4, column = 2 )
		global label4
		label4 = Label(mainContainer, text="")
		label4.configure(text="Waiting for a message...")
		label4.grid(row= 5, column = 2 )
		mainContainer.grid(row = 6, column = 2)
		x = threading.Thread(target=refresh)
		x.start()
		global message_a_envoyer
		message_a_envoyer = StringVar()
		global message_entry
		message_entry = ttk.Entry(screen1, textvariable = message_a_envoyer)
		message_entry.grid(row = 7, column = 2)
		ttk.Button(screen1, text="Envoyer", command = envoyer_un_message).grid(row = 8, column = 2)


	except Exception as error:
		print(error)








def main_screen():
	global screen
	screen = Tk()
	screen.geometry("300x250")
	screen.title("Projet Y")
	global servername
	global serverport
	serverport = StringVar()
	servername = StringVar()
	Label(screen, text = "").grid(row = 0, column =1 )
	Label(screen, text = 'Server Name :').grid(padx = 100, column = 2 )
	servername_entry1 = ttk.Entry(screen,textvariable = servername)
	servername_entry1.insert(0, "Hypérion")
	servername_entry1.grid(row= 3, column = 2 )
	Label(screen, text = 'Server Port :').grid(row= 4, column = 2 )
	serverport_entry = ttk.Entry(screen,textvariable = serverport)
	serverport_entry.insert(0, "8236")
	serverport_entry.grid(row= 5, column = 2 )
	ttk.Button(screen, text = "Connect", command = login_verify ).grid(row= 6, column = 2 )
	screen.mainloop()


main_screen()

