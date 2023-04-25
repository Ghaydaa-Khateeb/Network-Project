from socket import *
import pandas as pd 
import re
import os
serverPort = 5000 # port number = 5000
serverSocket = socket(AF_INET, SOCK_STREAM) #TCP Connection
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Now, The server is ready for recieving ... ")#the client in this case is our browser : google chrome
#go through infinite loop to recieve any requists from the client
while True:
	connectionSocket, addr = serverSocket.accept()  #accepting request
	sentence = connectionSocket.recv(1024).decode() #decoding the request
	urlAddres = sentence.split()[1] #storing the url address of our request
	print(addr) # printing the request message and the address
	# --------------------------------------------------------------------------
	# ---- check if one of the requested file doesn't exisit -------------------
	if urlAddres.endswith('.css'):
		css_name = urlAddres.split('/')[1]
		if os.path.isfile(css_name) == False:
			urlAddres = "error"
	elif urlAddres.endswith('.html'):
		html_name = urlAddres.split('/')[1]
		if os.path.isfile(html_name) == False and html_name != 'index.html':
			urlAddres = "error"
	elif urlAddres.endswith('.png'):
		if(urlAddres.split('/')[1] == 'images'):
			image_name = urlAddres.split('/')[2]	
		else:
			image_name = urlAddres.split('/')[1]
		Path = os.path.join('images', image_name)
		if os.path.isfile(Path) == False:
			urlAddres = "error"
	elif urlAddres.endswith('.jpg'):
		if(urlAddres.split('/')[1] == 'images'):
			image_name = urlAddres.split('/')[2]	
		else:
			image_name = urlAddres.split('/')[1]
		Path = os.path.join('images', image_name)
		if os.path.isfile(Path) == False:
			urlAddres = "error"	
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	print(sentence)
	if(urlAddres == '/') or (urlAddres == '/index.html'):#opening the main.html
		mainHTML = open('main.html') #opening the file
		readHTML = mainHTML.read() #reading the html file
		mainHTML.close()
		connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())  
		connectionSocket.send('Content-Type: text/html \r\n'.encode()) 
		connectionSocket.send('\r\n'.encode())  # End of the header of the response.
		connectionSocket.send(readHTML.encode()) # sending the response data
	elif urlAddres.endswith('.css'):#if the request is for a css file
		css_name = urlAddres.split('/')[1] #storing the name of the requested css file
		mainCss = open(css_name)# opening the file
		readCss = mainCss.read()# reading the file
		mainCss.close()
		if os.path.isfile(css_name) == True:
			connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())  
			connectionSocket.send('Content-Type: text/css \r\n'.encode()) 
			connectionSocket.send('\r\n'.encode())  # End of the header of the response.
			connectionSocket.send(readCss.encode())
	elif urlAddres.endswith('.jpg') or urlAddres.endswith('.jpg/'):#if the request is for a jpg file
		if(urlAddres.split('/')[1] == 'images'):#storing the name of the jpg photo
			image_name = urlAddres.split('/')[2]	
		else:
			image_name = urlAddres.split('/')[1]
		Path = os.path.join('images', image_name)# here we make the url address for the photo in our pc	
		if os.path.isfile(Path) == True:
			connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
			connectionSocket.send(('Content-Type: image/jpeg \r\n').encode())  
			connectionSocket.send('\r\n'.encode())# End of the header of the response.
			image = open(Path, 'rb')
			image_data = image.read()
			image.close()
			connectionSocket.send(image_data)
	elif urlAddres.endswith('.png') or urlAddres.endswith('.png/'):
		if(urlAddres.split('/')[1] == 'images'):
			image_name = urlAddres.split('/')[2]	
		else:
			image_name = urlAddres.split('/')[1]
		Path = os.path.join('images', image_name)
		if os.path.isfile(Path) == True :
			connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
			connectionSocket.send(('Content-Type: image/png \r\n').encode()) 
			connectionSocket.send('\r\n'.encode())# End of the header of the response.
			Path = os.path.join('images', image_name)# here we make the url address for the photo in our pc
			image = open(Path, 'rb')
			image_data = image.read()
			image.close()
			connectionSocket.send(image_data)
	elif urlAddres.endswith('.html'):#reading seperated html file
		fileName = urlAddres.split('/')[1];
		mainHTML = open(fileName)
		readHTML = mainHTML.read()
		mainHTML.close()
		if os.path.isfile(fileName):
			connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())  
			connectionSocket.send('Content-Type: text/html \r\n'.encode()) 
			connectionSocket.send('\r\n'.encode())  # End of the header of the response.
			connectionSocket.send(readHTML.encode())
	elif urlAddres == "/sortByName" or urlAddres == "/sortByName/":#sorting the csv data according to the name
		connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
		connectionSocket.send('Content-Type: text/plain \r\n'.encode())  
		connectionSocket.send('\r\n'.encode())
		data   = pd.read_csv('data.csv')  
		names  = data.iloc[:, 0].values  #first column - Names
		prices = data.iloc[:, 1].values  #second column - Prices
		#bubble sort algorithm 
		for i in range(0 , len(names)):
			for j in range(i + 1, len(names)):
				if names[j] < names[i]:
					names[i], names[j] = names[j], names[i]     #swapping
					prices[i], prices[j] = prices[j], prices[i] #swapping
		#printing the results as a text/plain
		message = "Names" + " " * (25) + "--->  Prices\n"
		message += "==========================================\n"
		for i in range(0, len(names)): 
			message += str(names[i]) + " " * (30 - len(names[i])) + "--->    " + str(prices[i]) + "\n"
			message += '------------------------------------------' + '\n'
		connectionSocket.send(message.encode())#sending the data
	elif urlAddres == "/sortByPrice" or urlAddres == "/sortByPrice/":
		connectionSocket.send('HTTP/1.1 200 ok\r\n'.encode())
		connectionSocket.send('Content-Type: text/plain \r\n'.encode())  
		connectionSocket.send('\r\n'.encode())
		data   = pd.read_csv('data.csv')  
		names  = data.iloc[:, 0].values  #first column - Names
		prices = data.iloc[:, 1].values  #second column - Prices
		#bubble sort algorithm 
		for i in range(0 , len(prices)):
			for j in range(i + 1, len(prices)):
				if prices[j] < prices[i]:
					prices[i], prices[j] = prices[j], prices[i] #swapping
					names[i], names[j] = names[j], names[i]     #swapping
		#printing the results as a text/plain
		message = "Names" + " " * (25) + "--->  Prices\n"
		message += "==========================================\n"
		for i in range(0, len(names)): 
			message += str(names[i]) + " " * (30 - len(names[i])) + "--->    " + str(prices[i]) + "\n"
			message += '------------------------------------------' + '\n'
		connectionSocket.send(message.encode()) #sending the data
	else:
		error_404 = open('404.html')#opening 404.html
		error_404_read = error_404.read() #reading the file
		error_404.close()
		idx = 0
		i1 = 0
		i2 = 0
		#replacing _ with ip and port numbers
		for i in range(0 , len(error_404_read)):
			if error_404_read[i] == '_':
				i1 = i
		error_404_read = error_404_read[0 : i1] + str(addr[1]) + error_404_read[i1 + 1 : ]
		for i in range(0 , len(error_404_read)):
			if error_404_read[i] == '_':
				i2 = i
		error_404_read = error_404_read[0 : i2] + str(addr[0]) + error_404_read[i2 + 1 : ]
		connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())  
		connectionSocket.send('Content-Type: text/html \r\n'.encode())
		connectionSocket.send('\r\n'.encode())# Ending the header lines in the response
		connectionSocket.send(error_404_read.encode()) 	
	connectionSocket.close()
