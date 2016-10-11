from bs4 import BeautifulSoup as bs
import requests as r
import urllib as ul
from os import listdir as ls
from random import randint as rand

#funciones que ayudaran un poco.

abc="abcdefghijklmjopqrstuvwxyz"
abc=abc+abc.upper()+"1234567890_"

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
	try:
		return str(int(q)+1)
	except:
		return str(q)+random_string(3)

def setfilename(dire,name="1",ext=".txt"):
	if name+ext in ls(dire):
		return setfilename(dire,add(name),ext)
	else:
		return name+ext

def down(url,dest,filename="download",ext=".txt"):
	f=open(dest+setfilename(dest,filename,ext),"w")
	f.write(r.get(url).content)
	f.close()

#Luis Albizo 09/10/16
