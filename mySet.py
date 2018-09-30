#set ADT, need the array first
import carray
class Set(object):
	def __init__(self, lyst = ""):
		# O(n)
		if lyst == "":
			self.listset = [] #initialise empty set
		else: #initialise another set based on the inputed list/Array
			assert isinstance(lyst, list) or isinstance(lyst, carray.Array), "Optional parameter must be a list/Array ADT"
			self.listset = []
			for item in lyst:
				if item not in self.listset:
					self.listset.append(item)

		self.i = 0

	def __len__(self):
		# O(1) return length
		return len(self.listset)

	def __contains__(self, element):
		# O(1)
		if element in self.listset:
			return True
		else:
			return False

	def add(self, element):
		#O(1)
		if element not in self.listset:
			self.listset.append(element)

	def remove(self, element):
		#worse case O(n)
		if element in self.listset:
			self.listset.remove(element)
		else:
			raise ValueError('Element cannot be found in set')


	def __eq__(self, setB):
		# O(n)
		for item in self.listset:
			if item not in setB.listset or len(self.listset) != len(setB.listset):
				return False
		return True

	def __ne__(self,setB):
		#O(n)
		for item in self.listset:
			if item not in setB.listset or len(self.listset) != len(setB.listset):
				return True
		return False


	def __le__(self, setB): #check for subset
		for item in self.listset:
			if item not in setB.listset:
				return False
		return True

	def __lt__(self, setB):
		for item in self.listset:
			if item not in setB.listset and len(self.listset) >= len(otherset.listset):
				return False
		return True

	def __add__(self, setB):
		#O(2n)
		tempthing = Set()
		for item in self.listset:
			tempthing.add(item)

		for item in setB.listset:
			if item not in tempthing:
				tempthing.add(item)

		return tempthing

	def __and__(self, setB):
		#O(n)
		tempthing = Set()
		for item in self.listset:
			if item in setB.listset:
				tempthing.add(item)

		return tempthing

	def __str__(self):
		#O(1)
		tempstr = str(self.listset)
		ver1 = tempstr.replace("[", "")
		ver2 = ver1.replace("]", "")
		return "{" + ver2 + "}"

	def __iter__(self):
		return self

	def __getitem__(self,index):
		#O(1)
		assert index>=0 and index <len(self), "Set subscript out of range"
		return self.listset[index]

	def __next__(self):
		templist = self.listset
		if self.i < len(templist):
			i = self.i
			self.i += 1
			return templist[i]
		else:
			self.i = 0
			raise StopIteration()

