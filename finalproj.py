#importing the custom ADT libraries
import AVLtree
import carray
import mySet
import myStack
# import python libraries
import ast
import datetime

class contactbook():
	def __init__(self):
		#building the contact book

		#set the autoload feature to off (default) and check later to see if this is overridden
		self.autoload = False
		#checking for todays date
		self.today = int(datetime.datetime.today().strftime('%Y%m%d'))
		#initialising a tree for each attribute, each tree stores the location of the particular set of data in the masterlist 
		self.treedict = {"first name":AVLtree.AVLTree(), "last name": AVLtree.AVLTree(), "age": AVLtree.AVLTree(), "horoscope": AVLtree.AVLTree() , "phone number":AVLtree.AVLTree(), "birthday":AVLtree.AVLTree(),"birthday[MMDD]":AVLtree.AVLTree()}
		#masterlist where the data of the person is stored
		self.masterlist = carray.Array(0)
		#hardcoded date data and horoscope data
		self.daysinmonth = (31,29,31,30,31,30,31,31,30,31,30,31)
		self.horocompatibility = {"aquarius":["leo","sagittarius"],"pisces":["virgo","taurus"],"aries":["libra","leo"],"taurus":["scorpio","cancer"],"gemini":["sagittarius","aquarius"],"cancer":["capricorn","taurus"],"leo":["aquarius","gemini"],"virgo":["pisces","cancer"],"libra":["aries","sagittarius"],"scorpio":["taurus","cancer"],"sagittarius":["gemini","aries"],"capricorn":["taurus","cancer"]}
		
		#var is the status of the autoload, if autoload is successful, var will become true, if not var will be false and program will start setup
		var = False
		try:
			#read the database File, if file is not there (got error) exit the try statement and proceed to setup
			f = open("database.nuode","r")
			c = f.read()
			#check autoload status that's stored in the database and override self.autoload
			if c[0] == "T":
				self.autoload = True
			f.close()
			#will prompt if user wants to autoload in the future
			if self.autoload == False:
				print("Looks like there's existing data of your contacts... Do you want to load it?")
				if input("[Y/N] ") == "Y":
					#self.initload outputs the status of loading the data, if successful var will be set to True
					var = self.initload("secretcode")
			else:
				#since self.autoload is true, just load it
				var = self.initload("secretcode")
		except:
			pass
		
		if var == False:
			## set up ##
			#get the user's own data first
			self.mydata = carray.Array(7)
			print("\n## Setup ##\n")
			print("What is your first name?")
			#first name
			self.mydata[0] = input("first name > ")
			print("\nHello %s, please fill in the rest of the details and we're good to go!\n" % (self.mydata[0]))
			#last name
			self.mydata[1] = input('last name > ')
			#phone number
			#getformat is a function that only takes in numbers
			self.mydata[3] = self.getformat("phone number > ")
			print("Please input your birthday in the format YYYYMMDD")
			#birthday, pass 2 in getformat for only getting input of birthday
			self.mydata[2] = self.getformat("birthday > ",2)
			#auto calculate age
			self.mydata[4] = self.calcage(self.mydata[2])
			#birthday in MMDD format
			self.mydata[5] = int(str(self.mydata[2])[4:])
			#calculate horoscope 
			self.mydata[6] = self.horoscope(self.mydata[5])
			#add this set of data into the contactbook
			self.add(self.mydata)

	def calcage(self,num1):
		#calculate age by subtracting today's date with birthday
		y1 = int(str(self.today)[0:4])
		md1 = int(str(self.today)[4:])
		y2 = int(str(num1)[0:4])
		md2 = int(str(num1)[4:])
		age = y1 - y2
		if md1 - md2 < 0:
			age -= 1
		return age

	def horoscope(self,bday):
		#hardcoded horoscope by checking birthday month and day
		mmdd = int(bday)
		if mmdd >= 120 and mmdd <= 218:
			return "aquarius"
		elif mmdd >= 219 and mmdd <= 320:
			return "pisces"
		elif mmdd >= 321 and mmdd <= 419:
			return "aries"
		elif mmdd >= 420 and mmdd <= 520:
			return "taurus"
		elif mmdd >= 521 and mmdd <= 620:
			return "gemini"
		elif mmdd >= 621 and mmdd <= 722:
			return "cancer"
		elif mmdd >= 723 and mmdd <= 822:
			return "leo"
		elif mmdd >= 823 and mmdd <= 922:
			return "virgo"
		elif mmdd >= 923 and mmdd <= 1022:
			return "libra"
		elif mmdd >= 1023 and mmdd <= 1121:
			return "scorpio"
		elif mmdd >= 1122 and mmdd <= 1221:
			return "sagittarius"
		elif mmdd >= 1222 or mmdd <= 119:
			return "capricorn"
	
	def mapping(self,s):
		#this function maps the keys in the self.treedict dictionary to the location of that corresponding data in the list
		if s == "first name":
			return 0
		elif s == "last name":
			return 1
		elif s == "age":
			return 4
		elif s == "phone number":
			return 3
		elif s == "birthday":
			return 2
		elif s == "birthday[MMDD]":
			return 5
		elif s == "horoscope":
			return 6
		else:
			assert False, "Wrong map word..."

	def add(self,datadict="",response=True): #adding into contact book
		#O log n
		#check if a presexisting formatted array is passed in, if not do the setup again
		if datadict == "":
			userdata= carray.Array(7)
			userdata[0] = input("first name > ")
			userdata[1] = input('last name > ')
			userdata[3] = self.getformat("phone number > ")
			print("Please input birthday in the format YYYYMMDD")
			userdata[2] = self.getformat("birthday > ",2)
			userdata[4] = self.calcage(userdata[2])
			#birthday MMDD
			userdata[5] = int(str(userdata[2])[4:])
			#horoscope
			userdata[6] = self.horoscope(userdata[5])
			#confirm if user wants to add in the data
			if input("Confirm? [Y, N] ") != "Y":
				print("Cancelled...")
				return False
		else:
			userdata = datadict
		
		# adds the array of user's data into the master array of all the userdata, this returns the index in the masterlist where the user's data is found
		index = self.masterlist.add(userdata)

		#begin adding the index of the data in masterlist into each attribute tree, the node key in the tree will be user's own value of that attribute
		for item in self.treedict:
			tree = self.treedict[item]
			
			tree.insert(userdata[self.mapping(item)],index)
		#check if the parameter for a response if true or not
		if response == True:
			print("\nAll done! If you want to change anything, feel free to edit()\n")

	def edit(self,searchstring=""):
		#O log n
		#this function edits the data of a specific user

		#searchstring is the quicksearch feature where criteria already passed in

		#call search function; get actual index of the data stored in masterlist 
		number = self.search(searchstring)

		status = True #this to check if the whole process got any error or not
		# if item is not found, the error response alrdy given by search function
		if number != "False":
			#get user's data (actual reference)
			data = self.masterlist[number]

			#make a copy of the data
			copyofdata = self.copy(data)

			print("what attribute do you want to edit?")
			#time to get the user's attribute he wants to edit and his new value for it
			#mode picker parameter 1: want to also get user to input the value for the data, parameter 2: disallow age, birthday[MMDD] and horoscope 
			mode,value = self.modepicker(True,True)

			#edit the actual user's data
			#self.mapping used as mode is a string but need to get its repective integer
			data[self.mapping(mode)] = value
			if mode == "birthday":
				#edit age and birthday[MMDD] and horoscope too
				data[4] = self.calcage(value)
				data[5] = int(str(value)[4:])
				data[6] = self.horoscope(value)

			#ask user whether he wants to edit another attribute
			while input("Edit another attribute? [Y, N] ") == "Y":
				#disallow age and birthday[MMDD] horoscope for modepicker
				mode,value = self.modepicker(True,True)
				data[self.mapping(mode)] = value
				if mode == "birthday":
					#edit age and birthday[MMDD] and horoscope
					data[4] = self.calcage(value)
					data[5] = int(str(value)[4:])
					data[6] = self.horoscope(value)

			print("\nSaving...\n")
			#the exact array for that user's data in masterlist is already edited so just edit the attribute trees
			for item in self.treedict:
				#check if data of that attribute is affected
				if copyofdata[self.mapping(item)] != data[self.mapping(item)]:
					tree = self.treedict[item]

					#the key of the node where user's index is stored has changed, so do a delete the node from the tree then insert again
					
					oldkey = copyofdata[self.mapping(item)]
					newkey = data[self.mapping(item)]
					#delete node with old key
					if tree.delete(oldkey,number) == False:
						status = False #status becomes error
						break
					#insert node with newkey
					tree.insert(newkey, number)
			#check if my data is edited or not, update it if it is
			if copyofdata == self.copy(self.mydata):
				self.mydata = data
			#print the respective responses for the statuses
			if status == True:
				print("Done!\n")
			else:
				print("Error something went wrong\n")
	
	def delete(self,searchstring):
		#O log n
		#delete a user's data

		#call search function; get actual index of the data stored in masterlist 
		number = self.search(searchstring)
		
		#check if item is found, if it isnt error response already provided by search function
		if number != "False":
			#find the user's data 
			mydict = self.masterlist[number]

			if mydict == self.mydata:
				#cannot delete own data
				print("I'm sorry, you cannot delete your own data, try edit() instead...")
				return
			# get a last confirmation
			if input("Are you sure you want to delete? [Y/N] ") == "Y":
				status = True #set a status of the function to true first

				#for each attribute tree, delete the node where the user's data corresponds to
				for item in self.treedict:
					tree = self.treedict[item]
					#delete with key (user's own attribute) and its reference
					if tree.delete(mydict[self.mapping(item)],number) == False:
						status = False #deletion failed
						break
				#delete the userdata from the masterlist
				self.masterlist.pop(number)

				if status == False:
					print("something went wrong with the deletion")
				else:
					print("Deleted successfully...\n")
			else:
				print("Cancelled...")

	def search(self,stringy="",orstatus=False):
		# O (log n) for each search criteria
		#default to AND search, orstatus is to check whether user wants to do a search by OR
		#search for the user's data, stringy is the quicksearch feature where criteria already passed in
		kwargs = {}
		var = False #check whether user dont need to input the criteria manually

		if stringy != "":
			var = True #user donnid to input manually
			biglist = stringy.split(",") #formatting into each crteria
			for item in biglist:
				smalllist = item.split("=") #split to get the attribute, and the value
				if smalllist[0] not in self.treedict.keys(): #check if the attribute inputtted is a valid attribute
					print("Error: You need to use the exact keywords for attributes provided!\nRedirecting to normal search")
					kwargs = {}
					var = False # user needs to input the crtieria manually
					break
				else:
					#attibute in the criteria is valid
					if orstatus == False:
						# AND search will just store the criteria in kwargs dict
						kwargs[smalllist[0]] = smalllist[1]
					else:
						# OR search will just store the value of criteria in kwargs dict as a list (so as to accommodate different values for same attribute)
						if smalllist[0] in kwargs.keys():
							kwargs[smalllist[0]].append(smalllist[1])
						else:
							kwargs[smalllist[0]] = [smalllist[1]]
		
		#check if the data is formatted properly, if not then redirect to manual search
		for strattri in ["age","phone number","birthday","birthday[MMDD]"]:
			if strattri in kwargs.keys():
				try:
					if orstatus == False:
						#remove the white space and turn the value into int
						kwargs[strattri] = int(kwargs[strattri].replace(" ",""))
					else:
						#remove the white space and turn the value into int, do it for each item in the list
						thelist = kwargs[strattri]
						for i in range(len(thelist)):
							thelist[i] = int(thelist[i].replace(" ",""))
				except:
					print("Invalid value for",strattri,"...\nRedirecting to normal search")
					kwargs = {}
					var = False

		if var == False: #manual search
			print("\nPlease input search criteria for attributes")
			mode,value = self.modepicker() #get the chosen attribute and its value
			#add into the kwargs to store the criteria
			if orstatus == False:
				kwargs[mode] = value
			else:
				kwargs[mode] = [value]
			#check if user wants to add another criteria
			while(input("Add another criteria [Y/N] ") == "Y"):
				mode,value = self.modepicker()
				if orstatus == False:
					kwargs[mode] = value
				else:
					if mode not in kwargs.keys():
						#first time will initialise with list
						kwargs[mode] = [value]
					else:
						#not the first time, just append to the exising list
						stuff = kwargs[mode]
						stuff.append(value)
						kwargs[mode] = stuff
				
		if orstatus == False:
			### AND search ###

			#get the first attribute and its criteria
			firstmode = list(kwargs.keys())[0]
			firstvalue = kwargs[firstmode]

			tree = self.treedict[firstmode] #respective attribute tree
			#tree searching
			result = tree.search(firstvalue) #returns a list of indexes for masterlist whose user's data matches the first attributes requirments
			#removing the first mode
			kwargs.pop(firstmode)

			if result == None:
				print("Error subject not found") #not found 
				return "False"
			#make a copy of the result data 
			result = self.copy(result)
			resultcopy = self.copy(result)

			for item in kwargs:
				#now by process of elimination check the whether the data satisfies the other criterias
				for entry in resultcopy:
					#entry is index in masterlist
					data = self.masterlist[entry] #get that userdata
					if data[self.mapping(item)] != kwargs[item]: #if that userdata does not satisfy the crteria, remove it
						result.remove(entry)
		else:
			### OR search ###
			ultimateset = mySet.Set() #store all the possible user's indexes into a set so they dont overlap

			for item in kwargs:
				tree = self.treedict[item] #get that attibute tree
				bigl = kwargs[item] #wanted values for that criteria
				for wantedvalue in bigl:
					lol = tree.search(wantedvalue) #search for userdata that satisfy the criteria
					if lol != None: #check if the result isnt empty
						for item in lol: #add the possible indexes to the set
							ultimateset.add(item)
			result = ultimateset

		if len(result) == 0: #result is empty
			print("Error subject not found")
			return "False"
		elif len(result) > 1: #now get user to choose which data does he/she want
			print("\nThere is more than 1 option\n")
			#listing options available
			for i in range(len(result)):
				firstname = self.masterlist[result[i]][0]
				lastname = self.masterlist[result[i]][1]

				print("\t" + str(i) + ") " + firstname + " " + lastname + "")
				
			#enable error checking for input
			userindex = self.getformat("\nChoose a integer from 0 to " + str(len(result)-1) + " > ") #get numbers
			while(userindex < 0 or userindex > len(result)-1):
				print("Out of range....")
				userindex = self.getformat("\nChoose a integer from 0 to " + str(len(result)-1) + " > ")

			vartoreturn = result[userindex] #the chosen data's index in masterlist
			result = self.masterlist[vartoreturn] # the chosen data itself	
		else:
			vartoreturn = result[0]
			result = self.masterlist[vartoreturn]

		#displaying the result 
		name = result[0] + " " + result[1]
		bd = str(result[2])
		bd = bd[:4] + "/" +  bd[4:6] + "/" + bd[6:]
		hscope = result[6]
		myhscope = self.mydata[6]
		#check for horoscope compatibility
		if hscope in self.horocompatibility[myhscope]:
			compatibility = bcolors.OKGREEN + "Well suited for each other" + bcolors.ENDC
		else:
			compatibility = bcolors.FAIL + "Incompatible with this person" + bcolors.ENDC
		#displaying the result 
		print("\n### Info ###\nName: %s\nAge: %d\nPhone number: %d\nBirthday(YYYYMMDD): %s\nHoroscope: %s\nRelationship compatibility: %s\n" % (name, result[4], result[3], bd, hscope,compatibility))
		
		# return index which this data is found
		return vartoreturn

	def sort(self,mode=""):
		#On
		if mode == "":
			print("Pick an attribute you want to sort the data by:")
			mode = self.modepicker(False) #only get the mode, not the value
		elif mode not in self.treedict.keys():
			print("Choosen attribute not found, please use the exact phrase/word")
			return #error

		if input("Ascending? [Y/N] ") == "Y": #check ascending or descending
			#since age is generic, print in order of birthday instead, but need to get the opposite order tho
			if mode == "age":
				thelist = self.treedict["birthday"].descendprint()
			else:
				thelist = self.treedict[mode].ascendprint()
		else:
			if mode == "age":
				thelist = self.treedict["birthday"].ascendprint()
			else:
				thelist = self.treedict[mode].descendprint()
		#the returned data empty
		if len(thelist) == 0:
			print("Empty data, nothing to sort...")
			return
		elif len(thelist) > 20: #truncate the response
			print("\nFor readability, only first 20 entries will be shown")
			thelist = thelist[0:20]

		print("\nPrinting names of contacts sorted by",mode,"\n")
		#printing
		for i in range(len(thelist)):
			print("\t"+ str(i+1) + ".",self.masterlist[thelist[i]][0],self.masterlist[thelist[i]][1],"|| " + mode + ":",self.masterlist[thelist[i]][self.mapping(mode)])
		print() #formatting stuff

	def max(self,attribute="",overriderecursion=False):
		#O log n
		if attribute == "":
			attribute = self.modepicker(False) #get an attribute from user
		elif attribute not in self.treedict.keys():
			print("use the exact phrase for the attribute") #invalid attribute given
			return
		#valid attribute below
		if attribute == "birthday" and overriderecursion == False: # for birthday, the max should be oldest, so his birthday number is the smallest so get the min instead
			self.min("birthday",True)
			return
		if attribute == "birthday[MMDD]" and overriderecursion == False: #same for birthday in MMDD
			self.min("birthday[MMDD]",True)
			return
		result = self.treedict[attribute].highestvalue() #get highest value node from the attribute tree
		if result != None:
			print(result.key) #print the highest node's key
		else:
			print("Data is empty...") #tree empty

	def min(self,attribute="",overriderecursion=False):
		#O log n
		if attribute == "":
			attribute = self.modepicker(False) #get user to pick attribute
		elif attribute not in self.treedict.keys():
			print("use the exact phrase for the attribute") #invalid
			return
		if attribute == "birthday" and overriderecursion == False: # for birthday, the min should be youngest, so his birthday number is the biggest so get the max instead
			self.max("birthday",True)
			return
		if attribute == "birthday[MMDD]" and overriderecursion == False: #same for birthday MMDD
			self.max("birthday[MMDD]",True)
			return
		result = self.treedict[attribute].lowestvalue() #lowest value node
		if result != None:
			print(result.key) #print the node's key
		else:
			print("Data is empty...") #tree is empty

	def average(self,attribute): #get the average, currently only supports age
		# O(N)
		if attribute == "":
			attribute = self.modepicker(False) #get attribute only
		elif attribute not in self.treedict.keys():
			print("use the exact phrase for the attribute")
			return
		
		thelist = self.treedict[attribute].ascendprint() #the indexes of all the data in the masterlist
		
		if len(thelist) == 0:
			print("Nothing to average")
			return

		if attribute == "birthday" or attribute == "birthday[MMDD]" or attribute == "phone number" or attribute == "horoscope":
			print("This attribute is not suitable for averaging")
			return #hardcoded to error

		index = self.mapping(attribute)
		average = 0

		for i in range(len(thelist)):
			number = self.masterlist[thelist[i]][index] # number for that attribute
			if isinstance(number,str): #if the result was a string then error
				print("This attribute is not suitable for averaging")
				return
			average = average + number #add them together

		average = "{:.2f}".format(average/len(thelist)) #divide them to get mean and round off to 2dp
		print(average)
		

	def getformat(self,mystring, mode = 1):
		#get the proper input for numbers, "mystring" is the question to be asked
		#modes: age,phone number:1, date[YYYYMMDD]:2, date[MMDD]:3 
		try:
			preservedstring = input(mystring).replace(" ", "") #remove whitespce
			thingy = int(preservedstring) #try to turn into int
		except:
			print("Only input numbers, try again...")
			return self.getformat(mystring,mode) #recurse and try again
		if mode == 2:
			#date[YYYYMMDD]
			if len(str(thingy)) != 8:
				print("Need to have 8 digits and first digit cannot be 0")
				return self.getformat(mystring,mode) #recurse and try again
			else:
				s = str(thingy)
				year = int(s[:4])
				month = int(s[4:6]) #get the year, month and day
				day = int(s[6:])

				if month > 12 or day > self.daysinmonth[month-1] or (month == 2 and year % 4 != 0 and day > 28): #check if the day and month fits the year
					print("Invalid date...")
					return self.getformat(mystring,mode)
		if mode == 3:
			#date[MMDD]
			if len(preservedstring) != 4:
				print("Need to type in 4 digits only in the format MMDD")
				return self.getformat(mystring,mode) #recurse and try again
			else:
				s = str(thingy)
				month = int(s[:-2])
				day = int(s[-2:])

				if month < 1 or month > 12 or day > self.daysinmonth[month-1]:
					print("Invalid date...")
					return self.getformat(mystring,mode)
		return thingy

	def modepicker(self,includevalue = True,disallowage=False):
		print("\nPick an attribute: 'first name', 'last name', 'age', 'phone number, 'birthday', 'birthday[MMDD]', 'horoscope'.\nUse the exact phrase")
		mode = input("attribute > ") #pick an attribute
		if disallowage == True:
			while(mode not in self.treedict.keys() or mode=="age" or mode=="birthday[MMDD]" or mode=="horoscope"): #make sure cannot be unwanted response
				if mode not in self.treedict.keys(): 
					print("Use the exact phrase/word")
				else:
					print("Cannot edit this attribute, try editing birthday instead")
				mode = input("attribute > ")
		else:
			while(mode not in self.treedict.keys()): #check if attribute selected is valid
				print("Use the exact phrase/word")
				mode = input("attribute > ")

		if includevalue == True: #return mode and value
			if mode == "first name" or mode == "last name" or mode == "horoscope":
				value = input("value for this attribute > ") #get plain text
			else:
				if mode == "birthday":
					value = self.getformat("value for this attribute > ",2) #get birthday YYYYMMDD
				elif mode == "birthday[MMDD]":
					value = self.getformat("value for this attribute > ",3) #get birthday MMDD
				else:
					value = self.getformat("value for this attribute > ") # integer

			return mode,value
		else:
			return mode
	
	def save(self):
		#(O n)
		print("\nSaving... Don't close yet")
		
		#check if storage file is there, if not then create own
		f = open("database.nuode","w+")
		
		if self.autoload == True: #write the status of autoload
			f.write("T\n")
		else:
			f.write("F\n")
		
		f.write(str(self.today)+"\n") #write todays date

		#get mydata, convert to python list (for the ast function to work) and write into file
		s1 = str(self.copy(self.mydata))
		f.write(s1 + "\n")

		#get masterlist, convert to python list (for the ast function to work) and write into file
		s2 = str(self.copy(self.masterlist))
		f.write(s2 + "\n")

		#get the deleted stack for the masterlist
		f.write(str(self.masterlist.deleted) +"\n")

		#convert all the trees into strings, write strings to file via a dictionary treedict
		for item in self.treedict:
			tree = self.treedict[item]
			s3 = str(tree.printTree())
			self.treedict[item] = s3
		f.write(str(self.treedict) +"\n")

		f.close()
		print("Done, Have a nice day!\n")

	def rebuild(self,mystring):
		# calls functions that are O(n)
		test = ast.literal_eval(mystring) #convert string to actual datatype
		return self.rback(test) #actual tree rebuilding here

	def rback(self,mytuple): #background function of tree rebuilding
		# O(n)
		tree = AVLtree.AVLTree() #initialise a tree

		if mytuple != None:
			alldata = mytuple[1] #root node/tree's data
			tree.node = AVLtree.treeNode(alldata[0],alldata[1]) #turn the node with trees key and extra info
			tree.height = alldata[2] #set the trees height
			tree.balancefactor = alldata[3] #set the trees balancefactor
			tree.mytag = alldata[4] #set the trees tag

			tree.node.leftChild = self.rback(mytuple[0]) #recurse for left child
			tree.node.rightChild = self.rback(mytuple[2]) #recurse for right child

		return tree #return initialised tree

	def listtoarray(self,thelist): #turns list to my own Array adt
		#O n
		mylist = thelist

		if isinstance(mylist,list):
			mylist = carray.Array(len(thelist)) #initliase my array with same length as my list
			for i in range(len(thelist)): #loop through and also turn each element into an array also (in case of nested lists)
				mylist[i] = self.listtoarray(thelist[i])
		return mylist

	def copy(self,thelist): #turns the Array or list into a python list
		#O n
		mylist = thelist
		if isinstance(mylist,list) or isinstance(mylist,carray.Array):
			mylist = []
			for item in thelist:
				mylist.append(self.copy(item))
		return mylist

	def size(self): #return size of the contact book
		# O(1)
		return len(self.masterlist)

	def clear(self):
		#O(1)
		print() #formatting
		if input("Confirm? [Y/N] ") == "Y": #get user to confirm
			self.treedict = {"first name":AVLtree.AVLTree(), "last name": AVLtree.AVLTree(), "age": AVLtree.AVLTree(), "horoscope": AVLtree.AVLTree(), "phone number":AVLtree.AVLTree(), "birthday":AVLtree.AVLTree(), "birthday[MMDD]":AVLtree.AVLTree()} #re initialsie the self.treedict
			self.masterlist = carray.Array() #reset the masterlist
			self.add(self.mydata,False) #add my own data without a response 
			print("Cleared...")
		else:
			print("Cancelled...")

	def initload(self,myfilename=""):
		# O n
		if myfilename == "": #no file name
			print("\nError: Please input the filename(where data will be retrived) within the parentheses of the load function\n")
			return False
		elif myfilename != "secretcode": #want to init from another file
			print("\nAre you sure?\nDoing this will override/erase all existing entries in this contactbook\n")
			if input("[Y/N] ") != "Y":
				print("Cancelled...")
				return False
		else: #use secretcode passphrase to prevent accidental init from database.nuode in event of myfilename is empty
			myfilename = "database.nuode"

		print("\nLoading data...")
		try:
			f = open(myfilename,"r")
		except:
			print("Uh-oh.. Looks like the file you requested for can't be found :((")
			return False

		contents = f.read()
		biglist = contents.split("\n")
		if len(biglist) == 0:
			print("Uh-oh.. Looks like the file you requested for is empty :((")
			return False
		
		#get my data
		self.mydata = self.listtoarray(ast.literal_eval(biglist[2])) #first get the python list back using ast then convert back into my own array data structure!!
		#get masterlist
		self.masterlist = self.listtoarray(ast.literal_eval(biglist[3])) #convert back to my own array data structure!!

		bigstack = myStack.Stack(biglist[4]) #reinitialise stack for deleted indexes for masterslist
		self.masterlist.deleted = bigstack
		
		treedict = ast.literal_eval(biglist[5]) #get treedict back
		for item in treedict:
			finaltree = self.rebuild(treedict[item]) #rebuild trees
			self.treedict[item] = finaltree

		date = int(biglist[1]) #get the date the contact book was last saved
		f.close()
		bdaynamelist = ""

		#live age updating
		if self.today != date: #if the contact book has a different date then need to update the ages
			print("Updating ages...")
			
			affectedlist = self.treedict["birthday[MMDD]"].getfromrange(int(str(date)[4:]),int(str(self.today)[4:])) #get the indexes in masterlist of affected users (whose birthday lie between when the contact book is last opened and today)
			if affectedlist != None:
				for num in affectedlist:
					loldata = self.masterlist[num]
					oldage = loldata[4] #find the old age 
					loldata[4] = self.calcage(loldata[2]) # set it to the new age
					# do delete and insert operation for age tree for all the affected users
					self.treedict["age"].delete(oldage,num) #delete node with old age
					self.treedict["age"].insert(loldata[4],num) #add node with new age
					#birthday alert!!
					if loldata[5] == int(str(self.today)[4:]): #if the birthday of the user happens to be today, then append it to the birthday string
						congratsstring = "\t" + str(loldata[0]) + " " + str(loldata[1]) + " turns " + bcolors.OKGREEN + str(loldata[4]) + bcolors.ENDC + " today!" + "\n"
						bdaynamelist += congratsstring
			
		print("Done")
		print(bcolors.BOLD + "\nWelcome back,", self.mydata[0]," ٩(^ᴗ^)۶\n" + bcolors.ENDC)

		##feature get today's birthday people and print birthday message
		if bdaynamelist != "":
			print("\nIt's the following people's birthday today 🎂🎂\nDon't forget to wish them a happy birthday!\n")
			print(bdaynamelist)

		self.autoload = True #set self.autoload to true
		return True

	def load(self,filename): #load function that takes in more data and adds to contact book (in the end the database "nuode.database" will still be created)
		# O n
		try:
			f = open(filename,"r") #check if the file exist
		except:
			print("Uh-oh.. Looks like the file you requested for can't be found :((")
			return
		print("\nLoading data...")

		#uses a pre-set format of [firstname, last name, birthday, phone number] separated by "\n"
		
		contents = f.read()
		biglist = contents.split("\n")
		counter = 0 #counter for successful entries added
		negcounter = 0 #counter for unsuccessful entries added
		for smalllist in biglist:
			if smalllist != "":
				smalllist = ast.literal_eval(smalllist) #get the actual list

				#append the age
				smalllist.append(self.calcage(smalllist[2]))
				#append the birthday[MMDD]
				smalllist.append(int(str(smalllist[2])[4:]))
				#append the horoscope
				smalllist.append(self.horoscope(smalllist[5]))

				numberlist = self.treedict["first name"].search(smalllist[0]) #do a search by first name 
				if numberlist != None: #if there are existing entries with same first name
					myvar = True #set status true at first
					for index in numberlist:
						if self.masterlist[index] == smalllist: #if that set of data already exist, ignore it and increase negcounter by 1
							negcounter += 1
							myvar = False #status false
							break
					if myvar == True: #original entry so can add it into the contact book
						self.add(smalllist,False)
						counter += 1
				else: #no existing entries with same first name
					self.add(smalllist,False)
					counter += 1

		print("Done, added",counter,"new contacts.")
		if negcounter > 0:
			print("However,",negcounter, "entries were ommitted as they already exist")
		f.close()

#for printing in color in terminal	
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

print("\nWelcome to the contact book")
mybook = contactbook()

#User Interface

print("\nLet's get started... What would you like to do?\n<type 'exit()' to leave, type 'help()' for help>\n")
while True:
	userinput = input("contactbook(home) > ")
	if userinput=="add()":
		mybook.add()
	elif "edit(" in userinput:
		mybook.edit(userinput[5:-1])
	elif "orsearch(" in userinput:
		mybook.search(userinput[9:-1],True)
	elif "search(" in userinput:
		mybook.search(userinput[7:-1])
	elif "delete(" in userinput:
		mybook.delete(userinput[7:-1])
	elif "min(" in userinput:
		mybook.min(userinput[4:-1])
	elif "max(" in userinput:
		mybook.max(userinput[4:-1])
	elif "average(" in userinput:
		mybook.average(userinput[8:-1])
	elif "initload(" in userinput:
		mybook.initload(userinput[9:-1])
	elif "load(" in userinput:
		mybook.load(userinput[5:-1])
	elif "sort(" in userinput:
		mybook.sort(userinput[5:-1])
	elif userinput == "exit()":
		mybook.save()
		break
	elif userinput == "size()":
		print(mybook.size())
	elif userinput == "clear()":
		mybook.clear()
	elif userinput == "help()":
		print("\ntype:\n\t" + bcolors.BOLD + "add()" + bcolors.ENDC + " to add people\n\t" + bcolors.BOLD + "edit()" + bcolors.ENDC + " to edit a profile\n\t" + bcolors.BOLD + "search()" + bcolors.ENDC + " to search for a person (default is <AND> for multiple\n\tcriteria\n\t" + bcolors.BOLD + "orsearch()" + bcolors.ENDC + " to set search criteria when result only needs to\n\tsatisfy 1 of it <OR>)\n\t" + bcolors.BOLD + "delete()" + bcolors.ENDC + " to delete a profile\n\t" + bcolors.BOLD + "sort()" + bcolors.ENDC + " to list data sorted by that attribute (truncated to first\n\t20 entries)\n\t" + bcolors.BOLD + "save()" + bcolors.ENDC + " to export the contactbook to database.nuode filetype\n\t" + bcolors.BOLD + "load(<filename>)" + bcolors.ENDC + " to add some data on top on existing\n\tones (safe version)\n\t" + bcolors.BOLD + "initload(<filename>)" + bcolors.ENDC + " to load existing data into contactbook\n\t(!Warning this will override/erase all existing entries in\n\tcurrent session)\n\t" + bcolors.BOLD + "size()" + bcolors.ENDC + " to get the number of contacts\n\t" + bcolors.BOLD + "clear()" + bcolors.ENDC + " to remove all the data except yours\n\t(!Warning: cannot be undone)\n\t" + bcolors.BOLD + "max(), min() and average()" + bcolors.ENDC + " to get some meaningful data\n")
	else:
		print("Unrecognised command, type help() to seek help")


		