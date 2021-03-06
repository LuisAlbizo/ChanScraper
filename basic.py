from bs4 import BeautifulSoup as bs
import requests as r
import urllib as ul
from os import listdir as ls
from random import randint as rand

#funciones que ayudaran un poco.

abc="abcdefghijklmjopqrstuvwxyz"
abc=abc+abc.upper()+"1234567890_"

def get_meta_info(what,soup):
	try:
		return soup.find("meta",{"name":what})["content"]
	except:
		return str()

def get_ext(url):
	return url[-4:]

def fix_rel(url,prot="http"):
	if url[:len(prot)]==prot:
		return url
	else:
		if url[:2]=="//":
			return prot+":"+url
		else:
			return prot+":/"+url

def random_string(leng=5):
	gen=str()
	for el in range(0,leng):
		gen=gen+abc[rand(0,len(abc)-1)]
	return gen

def add(q):
	return random_string(3)+q

def setfilename(dire,name):
	if name in ls(dire):
		return setfilename(dire,add(name))
	else:
		return name

def down(url,dest,filename="download.txt"):
	f=open(dest+setfilename(dest,filename),"w")
	f.write(r.get(url).content)
	f.close()

#Luis Albizo 09/10/16
