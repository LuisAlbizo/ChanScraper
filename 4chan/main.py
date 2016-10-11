from basic import *
from os import system as sh, mkdir

class albizo:
	def __init__(self):
		self.__main_chan="http://www.4chan.org/"
		self.__board="http://boards.4chan.org"
		self.__actual_url=self.__main_chan
		self.boards=[]
		self.main_screen()

	def get_tab(self,url):
		return url[url.index("g")+1:]

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
			self.boards.append(el,":",tabs[el]["name"])
		self.display_listofboards()
		self.goto_board("/"+input("\nBoard: ")+"/")

	def display_listofboards(self):
		i=0
		while i<len(self.boards):
			try:
				print(self.boards[i]+"|"+self.boards[i+1]+"|"+self.boards[i+2])
				i+=3
			except:
				try:
					print(self.boards[i]+"|"+self.boards[i+1])
					break
				except:
					print(self.boards[i])
					break

	def get_threads(self,board_page):
		threads={}
		soup=bs(r.get(board_page).content)
		board=self.__actual_url
		print(board)
		tdb=soup.findAll("div",{"class":"thread"})
		i=1
		for el in tdb:
			op=el.find("div",{"class":"postContainer opContainer"})
			post_info=op.find("span",{"class":"name"}).text+op.find("span",{"class":"dateTime postNum"}).text
			postid=op.find("a",{"title":"Reply to this post"})
			file_info=op.find("div",{"class":"fileText"})
			file_url=fix_rel(file_info.find("a")["href"])
			file_info=file_info.text
			replys=str(op.find("span",{"class":"info"}).text)
			title_thread=str(op.find("span",{"class":"subject"}).text)
			message=str(op.find("blockquote",{"class":"postMessage"}).text)
			threads[i]={"post_info":post_info,"post_url":board+postid["href"]}
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
		print("Your request: "+board)
		self.__actual_url=self.__board+board
		sp=bs(r.get(self.__actual_url).content,"html.parser")
		print("Loading threads...")
		threads=self.get_threads(self.__actual_url)
		print("Displaying threads...")
		self.display_board(threads)

albizo()

#Luis Albizo 10/10/16
