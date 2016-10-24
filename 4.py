from basic import *
from os import system as sh, mkdir

"""
Este script no esta bien hecho, no esta modularizado y la clase no representa ningun objeto.
Solo se puede usar este script a travez de una interfaz consola (a menos que tu modifiques este codigo)
Probablememte tenga muchos errores, hice este script en poco tiempo (2 dias) y no segui ninguna logica.
Ten en cuenta eso cuando leas mi codigo porque ni yo lo entiendo.
"""

class FourchanScraper:
	def __init__(self,directory):
		self.directory=directory
		self.__main_chan="http://www.4chan.org/"
		self.__board="http://boards.4chan.org"
		self.__actual_url=self.__main_chan
		self.boards=[]
		self.acualboard=None
		self.main_screen()

	def get_tab(self,url):
		return url[url.index("g")+1:]

	def get_thread_files(self,url,directory):
		try:
			mkdir(self.directory+self.actualboard)
			mkdir(self.directory+self.actualboard+directory)
		except:
			try:
				mkdir(self.directory+self.actualboard+directory)
			except:
				pass
		print("Loading...")
		fsp=bs(r.get(url).content,"html.parser")
		files=fsp.findAll("div",{"class":"fileText"})
		c=len(files)
		i=0
		for el in files:
			current_file=el.find("a")
			try:
				filename=self.directory+self.actualboard+directory+current_file["title"]
			except:
				filename=self.directory+self.actualboard+directory+current_file.text
			f=open(filename,"wb")
			f.write(r.get(fix_rel(current_file["href"],"http")).content)
			f.close()
			i+=1
			print("(%i/%i) %s saved" % (i, c,filename.split("/")[-1])) 

	def view_thread(self,thread):
		tsp=bs(r.get(thread).content,"html.parser").find("div",{"class":"thread"})
		op=tsp.find("div",{"class":"postContainer opContainer"})
		print("OP\n")
		
	def main_screen(self,stats=True,long_tabs=False):
		sp=bs(r.get(self.__main_chan).content,"html.parser")
		tablones=sp.findAll("div",{"class":"boxcontent"})[1]
		temas=tablones.findAll("h3",{"style":"text-decoration: underline; display: inline;"})
		temtabs=tablones.findAll("ul")
		tabs=dict()
		if long_tabs:
			print("\t\tBoards")
		for el in range(0,len(temas)):
			if long_tabs:
				print(temas[el].text)
			for ele in temtabs[el].findAll("li"):
				if long_tabs:
					print("\t"+ele.text+" - "+self.get_tab(ele.find("a")["href"]))
				tabs[self.get_tab(ele.find("a")["href"])]={"url":fix_rel(ele.find("a")["href"]),"name":ele.text}
		if stats:
			print("\n\t\tStats\n")
			for el in sp.findAll("div",{"class":"stat-cell"}):
				print(el.text)
		print("\n\tChoose your board: \n")
		for el in tabs.keys():
			self.boards.append(el+"-"+tabs[el]["name"])
		self.display_listofboards()
		self.goto_board("/"+input("\nBoard: ")+"/")

	def display_listofboards(self):
		i=0
		while i<len(self.boards):
			try:
				print(self.boards[i]+" "+self.boards[i+1]+" "+self.boards[i+2])
				i+=3
			except:
				try:
					print(self.boards[i]+" "+self.boards[i+1])
					break
				except:
					print(self.boards[i])
					break

	def get_threads(self,board_page):
		threads={}
		soup=bs(r.get(board_page).content)
		board=self.__actual_url
		tdb=soup.findAll("div",{"class":"thread"})
		i=1
		for el in tdb:
			op=el.find("div",{"class":"postContainer opContainer"})
			post_info=op.find("span",{"class":"name"}).text+" "+op.find("span",{"class":"dateTime postNum"}).text
			postid=op.find("a",{"title":"Reply to this post"})
			try:
				file_info=op.find("div",{"class":"fileText"})
				file_url=fix_rel(file_info.find("a")["href"])
				file_info=file_info.text
			except:
				file_info=str()
				file_url=str()
			replys=str(op.find("span",{"class":"info"}).text)
			title_thread=str(op.find("span",{"class":"subject"}).text)
			message=str(op.find("blockquote",{"class":"postMessage"}).text)
			threads[i]={"post_id":postid,"post_info":post_info,"post_url":board+postid["href"].split("#")[0]}
			threads[i]["file_info"]=file_info
			threads[i]["file_url"]=file_url
			threads[i]["title"]=title_thread
			threads[i]["message"]=message
			threads[i]["replys"]=replys
			i+=1
		return threads

	def display_board(self,threads):
		for k in range(1,len(threads)+1):
			t=threads[k]
			print("\t[idshort]:"+str(k))
			print("Title: "+t["title"]+"\n"+"Info: "+t["post_info"])
			print(t["file_info"])
			print("Message:\n"+t["message"]+"\n\n"+t["replys"]+"\n")

	def goto_board(self,board):
		#Shows Message
		sh("clear")
		self.actualboard=board
		print("Your request: "+board)
		self.__actual_url=self.__board+board
		sp=bs(r.get(self.__actual_url).content,"html.parser")
		print(sp.find("title").text+"\n"+get_meta_info("description",sp))
		if sp.find("title").text[:3]=="404":
			print("404 - back to main")
			self.main_screen()
		print("Loading threads...")
		threads=self.get_threads(self.__actual_url)
		print("Displaying threads...")
		self.display_board(threads)
		while True:
			print("\n\tOptions:\n[i:download by idshort] [m:go to main] [c:change current page]\n[p:download all images of all threads in actual page]\n[v:view thread] [x:exit]")
			opc=input("option: ")
			if opc=="i":
				idshort=int(input("select idshort: "))
				self.get_thread_files(threads[idshort]["post_url"],input("directory: ")+"/")
			elif opc=="m":
				self.main_screen()
			elif opc=="c":
				page=input("Enter number of page: ")
				self.goto_board(self.actualboard+page)
			elif opc=="v":
				idshort=int(input("select idshort: "))
				self.view_thread(threads[idshort]["post_url"])
			elif opc=="p":
				for idshort in list(threads.keys()):
					#title=threads[idshort]["title"]
					#if title==str():
					title=threads[idshort]["post_id"].text
					print("Downloading thread: "+title)
					print("Downloading from: "+ threads[idshort]["post_url"])
					self.get_thread_files(threads[idshort]["post_url"],title+"/")
					print("%i of 15 threads completed" % (idshort))
			elif opc=="x":
				exit()

FourchanScraper("/sdcard/images/")

#Luis Albizo 10/10/16
