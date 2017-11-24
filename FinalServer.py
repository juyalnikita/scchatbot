#ChatServer_socketprogramming


import socket,os,sys
from threading import Thread,Lock
import random

Lock_thread=Lock()

#check message
def check_msg(msg):
	print('Checking')
	if (msg.find('JOIN_CHATROOM'.encode('utf-8'))+1):
		return(1)	
	elif (msg.find('LEAVE_CHATROOM'.encode('utf-8'))+1):
		return(2)
	elif (msg.find('DISCONNECT'.encode('utf-8'))+1):
		return(3)
	elif (msg.find('CHAT:'.encode('utf-8'))+1):
		return(4)
	elif (msg.find('KILL_SERVICE'.encode('utf-8'))+1):
		os.exit(1)
	elif (msg.find('HELLO'.encode('utf-8'))+1):
		return(5)
	else:
		return(6)

def join(conn_msg,csock):
	Lock_thread.acquire()
	gname = conn_msg.find('Join chatroom:'.encode('utf-8'))+14
	gname_end = conn_msg.find('\n'.encode('utf-8'))
	groupname = conn_msg[gname:gname_end]

	cname = conn_msg.find('CLIENT_NAME'.encode('utf-8'))+13
	cname_end = conn_msg.find(' '.encode('utf-8'),cname)
	clientname = conn_msg[cname:cname_end]
	rID = 0
	
	if (groupname.decode('utf-8')) == 'room1' :
		print('g1')
		g1_clients.append(c1Thread.socket)
		rID = 1001
	elif groupname == 'room2' :
		g2_clients.append(c1Thread.socket)
		rID = 1002
	#sending ackowledgement
	response = "JOINED_CHATROOM: ".encode('utf-8') + groupname+ "\n".encode('utf-8')
	response += "SERVER_IP: \n".encode('utf-8')
	response += "PORT: \n".encode('utf-8')
	response += "ROOM_REF: ".encode('utf-8') + str(rID).encode('utf-8') +'\n'.encode('utf-8')
	response += "JOIN_ID: ".encode('utf-8') + str(clThread.uid).encode('utf-8')   

	csock.send(response)
	return groupname,clientname

def leave(conn_msg,csock):   
	Lock_thread.acquire()
	grp_start = conn_msg.find('LEAVE_CHATROOM:'.encode('utf-8')) + 16
	grp_end = conn_msg.find('\n'.encode('utf-8'), grp_start)
	group_name = conn_msg[grp_start:grp_end]

	response = "LEFT_CHATROOM".encode('utf-8') + groupname + "\n".encode('utf-8')
	response += "JOIN_ID".encode('utf-8') + str(clThread.uid).encode('utf-8')

	grpmessage = "CLIENT_NAME:".encode('utf-8') + (c1Thread.clientname).encode('utf-8') + "\n".encode('utf-8')
	grpmessage += "CLIENT_ID:".encode('utf-8') + str(c1Thread.uid).encode('utf-8') +"\n".encode('utf-8')
	grpmessage += "LEFT GROUP".encode('utf-8')
	print(group_name)
	if (group_name.decode('utf-8')) == g1:
		i= g1_clients.index(c1Thread.socket)
		del g1_clients[i]
		for x in g1_clients:
			g1_clients[x].send(chat_text)
	elif group_name.decode('utf-8')) == g2:
		i=g2_clients.index(c1Thread.text)
		del g2_clients[i]
		for x in g2_clients:
			g2_clients[x].send(chat_text)
	csock.send(response)
	Lock_thread.release()

def chat(conn_msg,csock):       #msg_CHAT
	Lock_thread.acquire()		 
	chat_msg_start = conn_msg.find('MESSAGE:'.encode('utf-8')) + 9
	chat_msg_end = conn_msg.find('\n\n'.encode('utf-8'),chat_msg_start) - 1	

	chat_msg = conn_msg[chat_msg_start:chat_msg_end]

	grp_start = conn_msg.find('CHAT:'.encode('utf-8')) + 5
	grp_end = conn_msg.find('\n'.encode('utf-8'), grp_start) - 1

	group_name = conn_msg[grp_start:grp_end]
	
	chat_text = 'CHAT:'.encode('utf-8') + chat_msg + '\n'.encode('utf-8')			##change to Room number
	chat_text += 'CLIENT_NAME:'.encode('utf-8') +str(clThread.clientid).encode('utf-8')
	chat_text += 'MESSAGE: ' + chat_msg.encode('utf-8') 
	
	if group_name == g1:
		for x in g1_clients:
			(g1_clients[x].socket).send(chat_text)
	elif group_name == g2:
		for x in g2_clients:
			(g2_clients[x].socket).send(chat_text)
	Lock_thread.release()

def reply(msg,socket)
	msgstart=msg.find('HELLO:'.encode('utf-8'))+5
	msgend=msg.find('\n'.encode('utf-8'),msgstart)
	chatmsg=msg[msgstart:msgend]
			 
	response = "HELLO: ".encode('utf-8') + chat_msg + "\n".encode('utf-8')
	response += "IP: ".encode('utf-8') + str(clThread.ip).encode('utf-8') + "\n".encode('utf-8')
	response += "PORT: ".encode('utf-8') + str(clThread.port).encode('utf-8') + "\n".encode('utf-8')
	response += "StudentID: ".encode('utf-8') + "17307932".encode('utf-8') + "\n".encode('utf-8')
	
	socket.send(response)
			 
class client_threads(Thread):

	def __init__(self,ip,port,socket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.chatroom =[] 
		self.socket = socket
		self.uid = random.randint(1000,2000)
		self.roomname = ''
		self.clientname = ''
		self.roomID = ''

	def run(self):
		while True:
			conn_msg = csock.recv(1024)
			print(conn_msg)
			cflag=check_msg(conn_msg)
			print(conn_msg)
			cflag=check_msg(conn_msg)
			if cflag == 1 :
				 self.roomname,self.clientname,self.roomID = join(conn_msg,csock)
			elif cflag == 2 : leave(conn_msg,csock)
			elif cflag == 3 : return(0)
			elif cflag == 4 : chat(conn_msg,csock)
			elif cflag == 5 : response(conn_msg,csock)
			else : print('Error code - please wait.')					 #error code for incorrect message	
			self.chatroom.append(self.roomname)
			print('Clients in group g1:')
			print(len(g1_clients))
			print('Clients in group g2:')
			print(len(g2_clients))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = int(50000)
server.bind((host,port))
print(host)
thread_count = [] 

g1_clients = []         #group1
g2_clients = []         #group2


while True:
	server.listen(4)
	(csock,(ip,port)) = server.accept()

	print("Connected to ",port,ip)
	#monitoring connections

	clThread = client_threads(ip,port,csock)
	clThread.start()
	thread_count.append(clThread)
