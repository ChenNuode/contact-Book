#Static Array ADT
import myStack
import ctypes

class Array:
    def __init__(self, size=0):
        assert size >= 0 , "Array size must be > 0"
        self.deleted = myStack.Stack() #initialise the stack for deleted indexes
        self._size=size #size of slots that are currently used
        self._rsize=size #size of slots that have been used before
        self._actualsize=size + 5
        # Creates the array structure
        PyArrayType = ctypes.py_object * (size + 5)
        self._elements = PyArrayType()
        self.clear(None);

    # Return the length of the array
    def __len__(self):
        return self._size

    # Gets the content of the index element
    def __getitem__(self,index):
        if isinstance(index, slice):
            if index.step == None:
                steppy = 1
            else:
                steppy = index.step
            if index.start == None:
                startty = 0
            else:
                startty = index.start
            if index.stop == None:
                stoppy = self._size
            else:
                stoppy = index.stop

            arraynew = Array(int((stoppy - startty)/steppy))
            counter = 0
            for i in range(startty,stoppy,steppy):
                arraynew[counter] = self[i]
                counter += 1
            return arraynew
        else:
            assert index>=0 and index <self._rsize, "Array subscript out of range"
            return self._elements[index];

    #Sets a content in the index element
    def __setitem__(self, index, value):
        assert index>=0 and index <self._rsize, "Array subscript out of range"
        self._elements[index]=value

    #Clear the array by setting each element to the given value
    def clear(self,value):
        for i in range(self._rsize):
            self._elements[i]=value
        self.deleted = myStack.Stack()

    #Append an item to the back of the array OR to any spot that contains none
    def add(self,value):
        if self._actualsize - self._size == 0:
            self.recreatelist()

        if self.deleted.isEmpty() == True:
            self._elements[self._rsize] = value
            index = self._rsize
            self._rsize += 1
        else:
            index = self.deleted.pop()
            self._elements[index] = value
        self._size += 1
        return index

    #Self-enlarging array portion
    def recreatelist(self):
        newarray = Array(self._actualsize + 1)
        for i in range(self._rsize):
            newarray._elements[i] = self[i]
        PyArrayType = ctypes.py_object * (self._actualsize * 2)
        self._actualsize = self._actualsize * 2
        self._elements = PyArrayType()
        self.clear(None)
        for i in range(newarray._rsize):
            self._elements[i] = newarray[i]            
    
    #Deletion from array (turn that location into none and return the index at which deletion happened)
    def pop(self,index):
        assert index>=0 and index <self._rsize, "Array subscript out of range"
        self[index] = None
        self.deleted.push(index)
        self._size -= 1

    def copy(self):
        otherarray = Array(self._rsize)
        for i in range(self._rsize):
            otherarray[i] = self[i]
        return otherarray

    def __eq__(self,other):
        if len(self) != len(other):
            return False
        for i in range(self._rsize):
            if self[i] != other[i]:
                return False
        return True

    #Print the object
    def __str__(self):
        mystring = "["
        for item in self._elements[:self._rsize]:
            mystring = mystring + str(item) + ", "

        yay = mystring[:-2]
        yayfinal = yay + "]"

        return yayfinal

    #Returns an array iterator for traversing the elements
    def  __iter__ (self):
        return _ArrayIterator(self._elements[:self._rsize])

    
    #combining 2 arrays
    def extend(self,otherlist):
        assert isinstance(otherlist, Array), "Object must be an array"
        for item in otherlist:
            self.add(item)

#Iterator for the arrayADT
class _ArrayIterator:
    def __init__(self, theArray):
        self._arrayRef= theArray
        self._curNdx = 0

    def __iter__(self):
        return self

    def  __next__(self):
        if (self._curNdx < len(self._arrayRef)):
            entry = self._arrayRef[self._curNdx]
            self._curNdx+=1
            return entry
        else:
            raise StopIteration

if __name__ == "__main__":

    ####Client Code#######

    #initialise the array
    test = Array(10)

    #length of array
    print(len(test))
    
    #set item
    for i in range(len(test)):
        test[i] = Array(2)
    
    #get item
    print(test)
    
    #clear
    test.clear(None)

    for i in range(len(test)):
        test[i] = i+1
    
    #--append-- add
    test.add("test")



    #test2 = Array(15)
    #for i in range(len(test2)):
        #test2[i] = 5 * (i)

    #extend
    #test.extend(test2)

    #print
    print(test)

    #insert
    #test.insert(0, "first")
    #print(test)
    
    #pop
    test.pop(0)
    test.add("first")
    test.add("last")
    print(test)

    #slice
    print(test[3:7])

    #copy
    t = test.copy()

    #comparison
    if t == test:
        print("SUCCESS")

    #iterator
    for item in t:
        print(item)
    

#checked by nuode 6/9/18: all good

############     Account for time complexity       ############
#
# My time complexity is mostly O(n) with a few other functions as just O(k) with k as a constant
#
#  table of function | time complexity
#
#  __getitem__ slicing O(n)
#  clear O(n)
#  recreatelist O(2n)
#  extend O(n)
#  insert O(n)
#  pop O(n)
#  __str__ O(n)
# __iter__ O(n)
#

