from basic import down, bs, ul, fix_rel,r

class albizo:
	def __init__(self):
		self.__main_chan="http://www.4chan.org/"
		self.__board="http://boards.4chan.org"
		self.__actual_url=self.__main_chan
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
			print(el,":",tabs[el]["name"])

	def goto_board(self,board):
		self.__actual_url=self.__board+board
		sp=bs(r.get(self.__actual_url).content,"html.parser")
		print sp.find("title").text







albizo().init()

#Luis Albizo 10/10/16
