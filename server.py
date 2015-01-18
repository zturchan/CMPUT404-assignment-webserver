#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import os
import mimetypes
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
	#so we want to split up the request into manageable chunks
	requestLines = self.data.split("\r\n")
	line1Elements = requestLines[0].split(" ")
	requestType = line1Elements[0]
	requestedFile = line1Elements[1]
	#Disallow any sort of .. shenanigans
	if(requestedFile.startswith('/..')):
		self.request.send("HTTP/1.1 404 Not Found\r\n")
	#reroute unspecified files to index of their directory
	if(requestedFile[-1] == '/'):
		requestedFile += "index.html"
	if(requestType == "GET"):
		try:
			#Handle a get
			#get the requested file
			file = open("www/" + requestedFile, 'r')
			responseText = ""	
			for line in file:
				responseText += line
			self.request.send("HTTP/1.1 200 OK\r\n")
			mimetype, _= mimetypes.guess_type(requestedFile)
			#if(requestedFile.find(".css") != -1):
			#	self.request.send('Content-Type: text/css; encoding=utf8')
			#	print("css found in " + requestedFile)
			#else:
			self.request.send('Content-Type: ' + str(mimetype) + '; encoding=utf8\r\n')
			print("mimetype is " + str(mimetype))
			print("Response " + responseText)
			print("length" + str(len(responseText)))
			self.request.sendall('Content-Length'+ str(len(responseText)) + "\r\n")
			self.request.sendall('Connection: close' + "\r\n\r\n")
			self.request.sendall(responseText + "\r\n")
			print("sent")
		except:
			#self.request.send_error(404, "404 Not FOUND!")	
			self.request.send("HTTP/1.1 404 Not Found\r\n")
	else:
		self.request.send("HTTP/1.1 404 Not Found\r\n")
	self.request.close()
"""	parts = self.data.split("Host: ")
	hostparts = parts[1].split("\r\n")
	host = hostparts[0]
	print (host)	"""

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
