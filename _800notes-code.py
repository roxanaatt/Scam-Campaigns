import scampDB
import _800notes
import time



while (True):
	time.sleep(1200)
	
	Class800Notes = _800notes.C800notes()

	Baseurl = Class800Notes.baseurl
	#Baseurl = 'http://800notes.com/'

	soup = Class800Notes.Get_Page(Baseurl)

	phonebook = Class800Notes.Get_Phones(soup)
		
	for number in phonebook:
		print number
	 	NextURL = Class800Notes.Make_URL(number)
	 	print NextURL
	 	soup1 = Class800Notes.Get_Page(NextURL)
	 	NextPage=Class800Notes.Get_NextPage(soup1)
	 	#print NextPage
	 		
		while(NextPage is not None): 		
			time.sleep(10)
			listItem = Class800Notes.retBox(soup1)
			for item in listItem: 	
				comment = Class800Notes.Get_Comment(item)
				if comment is not None:
					print comment
				else:
					print "....CommentNone...."
					continue
						
				caller = Class800Notes.Get_Caller(item)
				if caller is not None:
					print "Calltype: "+ caller
				else:
					print "....NullCaller...."

				date = Class800Notes.Get_Date(item)
				if date is not None:
					print date
				else:
					print "....Null Date...."

				city = Class800Notes.Get_City(soup1)
				if city is not None:
					print "city: " + city
				else:
					print "....Null City...."

				country = Class800Notes.Get_Country(soup1)
				if country is not None:
					print "country: " + country
				else:
					print "....Null Country...."

				# state = Class800Notes.Get_State(soup1)
				# if state is not None:
				# 	print state
				# else:
				# 	print ".....Null state...."


				Class800Notes.store_DB(number,comment,date,country,city,caller,Baseurl)

			NextPage=Class800Notes.Get_NextPage(soup1)
			if NextPage is not None:
				soup1 = Class800Notes.Get_Page(NextPage)
				print NextPage
			else:
				print "....last page ....."
				NextPage = None

			
		time.sleep(10)	
		listItem = Class800Notes.retBox(soup1)
		for item in listItem: 	
			comment = Class800Notes.Get_Comment(item)
			if comment is not None:
				print comment
			else:
				print "....CommentNone...."
				continue
						
			caller = Class800Notes.Get_Caller(item)
			if caller is not None:
				print "Calltype: " + caller
			else:
				print "....NullCaller...."

			date = Class800Notes.Get_Date(item)
			if date is not None:
				print date
			else:
				print "....Null Date...."

			city = Class800Notes.Get_City(soup1)
			if city is not None:
					print "City: " + city
			else:
				print "....Null City...."

			country = Class800Notes.Get_Country(soup1)
			if country is not None:
				print "Country: " + country
			else:
				print "....Null Country...."

			# state = Class800Notes.Get_State(soup1)
			# if state is not None:
			# 	print state
			# else:
			# 	print ".....Null state...."

			Class800Notes.store_DB(number,comment,date,country,city,caller,Baseurl)

			



