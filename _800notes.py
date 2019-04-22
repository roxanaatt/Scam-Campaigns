import urllib2
import re
from bs4 import BeautifulSoup
#import time for tracing the error
import time
import argparse
import datetime
import os
from operator import itemgetter
import scampDB

#connection to DB


class C800notes:


	def __init__(self):
			
		self.baseurl = 'http://800notes.com'
		
		
#Get the http code of the page
	def Get_Page(self, baseurl):
		
		req = urllib2.Request(baseurl)
		req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0')
		response = urllib2.urlopen(req)
		the_page = response.read()
		soup = BeautifulSoup(the_page, 'html.parser')
		return soup

#make a phonebook of all the numbers in the website
	def Get_Phones(self, soup):
		phonebook = []
		#num = soup.find_all('div', attrs={'class':'oos_previewMain'}) 
		listItem = soup.find_all('div', attrs={'class':'oos_previewMain'}) 
		for row in listItem:
			res = row.find('h4', attrs={'class':'oos_previewHeader'})
			phone = res.find_all('a')
			for i in phone:
				print i.contents[0]
				phonebook.append(i.contents[0])
		return phonebook

#for each number make the url of the related page
	def Make_URL(self ,number):
		
		nextUrl = None
		#baseurl = self.baseurl
		nextUrl = 'http://800notes.com/Phone.aspx/' + number
		return nextUrl
	
#Retreive the whole box containing comment,caller,call type and timestamp for each person complain
	def retBox(self , soup1):
		
		div = soup1.find_all('div', attrs={'class':'oos_contlet'})
		return div

#Retreive the text of the comment
	def Get_Comment(self, divrow):
		
		row = divrow.find('div', attrs={"class":"oos_contletBody"})
		if row is None:
			description = None
		elif row is not None:
			description = row.text
		return description

#Retreive the time and date of the comment
	def Get_Date(self, divrow):

		i = divrow.find('time')
		if i is None:
			commentDate = None
		elif i.has_attr('datetime'):
			commentDate=(i['datetime'])
		
		return commentDate

#retreive caller and call type
	def Get_Caller(self, divrow):
		
		row1 = divrow.find('ul', attrs={"class":"callDetails"})
		if row1 is not None:
			call = row1.text.replace(' Caller: ','')
			Caller = call.replace('Call type: ','')
		

		elif row1 is None:
			Caller = 'None'
		return Caller

	# def Get_CallType(self, divrow):
		
	# 	row1 = divrow.find('ul', attrs={"class":"callDetails"})
	# 	if row1 is not None:
	# 		Caller = row1.text
	# 	elif row1 is None:
	# 		Caller = 'None'
	# 	return Caller



	def Get_City(self,soup):
		string = soup.find('div', attrs={'style':'padding-top:16px'})
		if string is not None:
			location = string.text.split(':')
		else:
			location = None

		if location is not None:
			if len(location)==3:
				city = location[2].replace(' ','')
			
			if len(location)==2:
				if (location[0] == ' Location'):
					city = location[1].replace(' ','')
				else:
					city = None	
		else:
			city = None 

		return city

	def Get_Country(self,soup):
		strings = soup.find('div', attrs ={'style':'padding-top:16px'})
		if strings is not None:
			location = strings.text.split(':')
		else:
			location = None

		if location is not None:
			if len(location)==3:
				country = location[1].replace(' ','').replace('Location','')

			if len(location)==2:
				if (location[0] == ' Country'):
					country = location[1].replace(' ','')
		else:
			country = None

		return country

	def Get_State(self,soup):
		strings = soup.find('div', attrs ={"class":"oos_paddedSection"})
		if strings is not None:
			count = strings.find_all('div')
		else:
			count = None
		if count is not None and len(count)>1:
			c = str(count[1])
		else:
			c = None
		if c is not None:
			countr= c.split("<br/>")
		else: 
			countr =None
		if countr is not None and len(countr)>2:
			d = countr[2]
		else:
			d = None
		if d is not None:
			f= d.split("<")
		else:
			f = None
		if f is not None:
			state = f[0].replace("Location: ","")
		else:
			state = None
		return state


#check if this comment has already been saved in DB or not and then save it to DB

	def store_DB(self,number,comment,date,country,city,caller,domain):
		db = scampDB.DB()
		cur1=db.get_cursor("info_cur",True)
		cur1.execute('''SELECT sc_tellnum, sc_date,sc_comment FROM tbl_scamcall WHERE sc_tellnum=%s AND sc_comment =%s AND sc_date=%s''',(number,comment,date))
		if cur1.rowcount > 0:
			print "---------Repeated-------------"
			
		elif cur1.rowcount == 0:
			#cur.execute('''INSERT INTO tbl_info(info_tellnum,info_comments,info_date,info_caller,info_calltype,info_webname) 
			#	VALUES (%s,%s,%s,%s,%s,%s)''',(title,description,commentDate,Caller,Caller,nextUrl))
			cur1.execute('''INSERT INTO tbl_scamcall(sc_tellnum,sc_comment,sc_date,sc_country,sc_state,sc_city,sc_calltype,sc_domain) 
				VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',(number,comment,date,country,'Null',city, caller,domain))
			db.commit()
			print "---------Add a new row-----------"
			

#Find the next pages for each number
	def Get_NextPage(self, soup):
		NextPage = None
		strings = soup.find('div', attrs={"class":"oos_pager"})
		if strings is not None:
			href = strings.find_all('a',attrs ={"class":"oos_wideOnly"}, href = True)
			for i in href:
				names = i.contents[0]
				fulllink = i.get('href')	
				if names == 'Next' or names == ' Next' or names == 'Next ' or names == ' Next ':
					NextPage = 'http://800notes.com'+fulllink
		else:
			NextPage = None

		return NextPage



		#Nexturl = None
		# if len(strings) == 0:
		# 	#print("This is the end of the pages")
		# 	return None
		
		# elif len(strings) !=0:
		# 	for string in strings:
	 # 			href = string.get('href')
	 # 			parturl = href
	 # 			Nexturl = ('http://800notes.com'+parturl)
	 # 			previousurl = Nexturl
	 # 		#Nexturl = None		
	 		
	 		
	 # 			if Nexturl == previousurl :
	 # 				return None
	 # 			else:
		#  			return Nexturl
	 		




