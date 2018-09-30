#class for node
class treeNode():
  #initialisation
  def __init__(self,key,extrainfo,leftc=None,rightc=None):
    # O1 time complexity

    #assign key (score or box office)
    self.key = key
    #assign extra info --> a list of tuples, each one contains all the data of each entry (score,boxoffice,rating,title...etc) 
    if isinstance(extrainfo, list):
      self.extrainfo = extrainfo
    else:
      self.extrainfo = [extrainfo]
    #assign the links to the children, empty child first
    self.leftChild = leftc
    self.rightChild = rightc
    
    
class AVLTree:
  def __init__(self):
    # O(1) time
    # creates empty node, height refers to the level of the node in tree, balance factor checks the whether the tree is balanced or not and mytag is the tree' tag
    self.node = None
    self.height = 1
    self.balancefactor = 0
    self.mytag = "even"
    
  def insert(self,newNode,extrainfo):
    # O(log2 N) time

    if self.node == None:
      #its an empty node
      self.node = treeNode(newNode,extrainfo) #creates a node
      #assigns empty nodes for children
      self.node.leftChild = AVLTree() 
      self.node.rightChild = AVLTree()
      
    else:
      #navigation
      if newNode > self.node.key:
        #navigates rightwards
        self.node.rightChild.insert(newNode,extrainfo)
        #calculates its new height relative to its children
        self.calheight()
      elif newNode < self.node.key:
        #navigates leftwards
        self.node.leftChild.insert(newNode,extrainfo)
        #calculates its new height relative to its children
        self.calheight()
      elif newNode == self.node.key:
        #found a node of same box office, gonna append its data to its self.extrainfo list
        self.node.extrainfo.append(extrainfo)
    # based on the new height, update the balance factors and tags    
    self.setbfactor()
  
  def setbfactor(self,mybool=1):
    #time O(1)
    if self.node != None:
      if self.node.leftChild.node != None or self.node.rightChild.node != None:
        # above statements make sure this is not a leaf node
        if self.node.leftChild.node == None:
          self.balancefactor = self.node.rightChild.height
          self.mytag = "rightheavy"
          #setting node as right heavy as theres no left child
        elif self.node.rightChild.node == None:
          self.balancefactor = self.node.leftChild.height
          self.mytag = "leftheavy"
          #setting node as left heavy as theres no right child
        else:
          #getting the balance factor and finding out which side is heavier
          self.balancefactor = abs(self.node.leftChild.height-self.node.rightChild.height)
          if self.node.leftChild.height < self.node.rightChild.height:
            self.mytag = "rightheavy"
          elif self.node.leftChild.height > self.node.rightChild.height:
            self.mytag = "leftheavy"
          else:
            # perfectly height balanced
            self.mytag = "even"
        # mybool tells it whether it wants to allow the rebalancing to trigger ornot, this will be set to 0 during rotations as its gonna give a recursion error otherwise 
        if mybool == 1:
          # when tree is too height unbalanced (diff > 2), start to autobalance itself, checks this recursively for sets of 3
          if self.balancefactor >= 2:
            self.dobalancing()
  
  def dobalancing(self):
    #time O(1)
    # this function decides how the tree should rotate
    if self.mytag == "leftheavy":
      if self.node.leftChild.mytag == "rightheavy":
        #performs a leftright rotations, else then just the right rotation
        self.node.leftChild.leftrotate()
      self.rightrotate()
      
    elif self.mytag == "rightheavy":
      if self.node.rightChild.mytag == "leftheavy":
        #performs a rightleft rotations, else then just the left rotation
        self.node.rightChild.rightrotate()
      self.leftrotate()
  
  def leftrotate(self):
    # time  O(3)
    #left rotation:
    #
    # a              b
    #  \            / \
    #   b    --->  a   c
    #  / \          \
    # d*  c          d*

    #assigning references for old positions
    oldtop = self.node 
    oldrighttree = oldtop.rightChild
    oldright = oldtop.rightChild.node
    
    # The left child of right child of root node before rotation be None (look at d above)
    oldrightlefttree = oldright.leftChild
    oldrightleft = oldright.leftChild.node 
    
    # reasigning the nodes
    self.node = oldright
    #previous root becomes the leftchild of new root
    oldright.leftChild.node = oldtop
    
    #checks if left child of right child of old root is none, 
    if oldrightleft == None:
      #if it is might as well create an empty node at its place
      oldtop.rightChild = AVLTree()
    else:
      #else transfer all stuff: node,height,mytag,balancefactor over
      oldtop.rightChild.node = oldrightleft
      oldtop.rightChild.height = oldrightlefttree.height
      oldtop.rightChild.mytag = oldrightlefttree.mytag
      oldtop.rightChild.balancefactor = oldrightlefttree.balancefactor
    
    a = oldtop.leftChild.height
    b = oldrightlefttree.height
    if oldtop.leftChild.node == None:
      a = 0
    if oldrightleft == None:
      b = 0
    #updates the height of the nodes
    oldright.leftChild.height = max(a,b) + 1
    #updates balances without triggering the rotation again
    oldright.leftChild.setbfactor(0)
    self.height = max(oldright.leftChild.height,oldright.rightChild.height) + 1
    #updates balances without triggering the rotation again
    self.setbfactor(0)
    
  def rightrotate(self):
    # time  O(3)
    #right rotation:
    #
    #     a           b
    #    /           / \
    #   b    --->   c   a
    #  / \             /
    # c   d*          d* 

    #assigning references for old positions
    oldtop = self.node
    oldlefttree = oldtop.leftChild
    oldleft = self.node.leftChild.node
    
    # The right child of left child of root node before rotation be None (look at d above)
    oldleftrighttree = oldleft.rightChild
    oldleftright = oldleft.rightChild.node 

    #assigning the nodes
    self.node = oldleft
    
    oldleft.rightChild.node = oldtop
    
    #checks if right child of left child of old root is none, 
    if oldleftright == None:
      #let empty node takes its place
      oldtop.leftChild = AVLTree()
    else:
      #transfer all stuff: node,height,mytag,balancefactor over
      oldtop.leftChild.node = oldleftright
      oldtop.leftChild.height = oldleftrighttree.height
      oldtop.leftChild.mytag = oldleftrighttree.mytag
      oldtop.leftChild.balancefactor = oldleftrighttree.balancefactor

    if oldtop.leftChild.node != None and oldtop.rightChild.node != None:
      oldleft.leftChild.height = max(oldtop.leftChild.height,oldtop.rightChild.height) + 1
      oldleft.leftChild.setbfactor(0)
    
    a = oldtop.rightChild.height
    b = oldleftrighttree.height
    if oldtop.rightChild.node == None:
      a = 0
    if oldleftright == None:
      b = 0
    #updates the height of the nodes
    oldleft.rightChild.height = max(a,b) + 1
    #updates balances without triggering the rotation again
    oldleft.rightChild.setbfactor(0)
    self.height = max(oldleft.leftChild.height,oldleft.rightChild.height) + 1
    #updates balances without triggering the rotation again
    self.setbfactor(0)
         
  def getRight(self):
      #time O(1) returns object at rightchild
      return self.node.rightChild

  def getLeft(self):
      #time O(1) returns object at leftchild
      return self.node.leftChild

  def getRootVal(self):
      #time O(1) returns key of root
      return self.node.key
        
  def inorder(self, a, b,lyst,ainclusive = False,binclusive = False,reverse=False):
    # time O(n), N might not mean the whole length of the dataset, can be the length of a subset of it (explained in traversal function)
    if self.node != None:
      #recurse left if reverse is not false, else vice versa
      if reverse == False:
        self.node.leftChild.inorder(a,b,lyst,ainclusive,binclusive,reverse)
      else:
        self.node.rightChild.inorder(a,b,lyst,ainclusive,binclusive,reverse)
      #just check for the parameters and apply them, lyst appends the first thing in the tuple (shld be movie title)
      if ainclusive == True:
        if binclusive == True:
          if self.node.key >= a and self.node.key <= b:
            for item in self.node.extrainfo:
              #lyst.append(item[0])
              lyst.append(item)
        else:
          if self.node.key >= a and self.node.key < b:
            for item in self.node.extrainfo:
              #lyst.append(item[0])
              lyst.append(item)
      else:
        if binclusive == True:
          if self.node.key > a and self.node.key <= b:
            for item in self.node.extrainfo:
              #lyst.append(item[0])
              lyst.append(item)
        else:
          if self.node.key > a and self.node.key < b:
            for item in self.node.extrainfo:
              #lyst.append(item[0])
              lyst.append(item)
      #recurse right if reverse is not false, else vice versa
      if reverse == False:
        self.node.rightChild.inorder(a,b,lyst,ainclusive,binclusive,reverse)
      else:
        self.node.leftChild.inorder(a,b,lyst,ainclusive,binclusive,reverse)
    #output the list it generated
    return lyst
    
    
  def traversal(self, comparisonfactor1, comparisonfactor2,ainclusive=False,binclusive=False,reverse=False):
    # worse case (Olog2n), should be lesser than that, aim is to shorten the tree to isolate the area of the tree that needs to be inorder search 
    if self.node == None:
      #if root node is empty
      return None
    elif comparisonfactor1 > self.node.key and comparisonfactor2 > self.node.key:
      #narrow the inorder to rightchild object
      return self.node.rightChild.traversal(comparisonfactor1, comparisonfactor2,ainclusive,binclusive)
    elif comparisonfactor1 < self.node.key and comparisonfactor2 < self.node.key:
      #narrow the inorder traversal to leftchild object
      return self.node.leftChild.traversal(comparisonfactor1, comparisonfactor2,ainclusive,binclusive)
    else:
      # the upper and lower bound parameters are on both slides of tree so need to traverse whole tree
      if reverse == False:
        lyst = self.inorder(comparisonfactor1, comparisonfactor2,[],ainclusive,binclusive)
      else:
        lyst = self.inorder(comparisonfactor1, comparisonfactor2,[],ainclusive,binclusive,True)
      return lyst

  def ascendprint(self):
    #time (O1) but it calls functions that are O(N)
    #return the list of every title in sorted ascending order, uses the range: [lowestvalue(),highestvalue()]
    if self.node != None:
      return self.traversal(self.lowestvalue().key,self.highestvalue().key,True,True)
    else:
      return []
        
  def highestvalue(self):
    # time O(log2N)
    #loop to the highest value
    if self.node != None:
      current = self
      while(current.node.rightChild.node is not None):
        current = current.node.rightChild
      return current.node 
  
  def lowestvalue(self):
    if self.node != None:
      # time O(log2N)
      #loop to the lowest value
      current = self
      while(current.node.leftChild.node is not None):
        current = current.node.leftChild
      return current.node 

  def search(self,key):
    # time O(log2N)
    if self.node == None:
      #cant find anything search failed
      return None
    if self.node.key == key:
      #object located
      return self.node.extrainfo
    elif self.node.key < key:
      # recurse rightwards
      return self.node.rightChild.search(key)
    elif self.node.key > key:
      # recurse leftwards
      return self.node.leftChild.search(key)
  
  def deleteRecurse(self,key,extrastuff,replacement=""):
    # time O(log2n) worse case      
    if self.node == None:
      return False #cant find node to delete
    else:
      if self.node.key == key:
        #node that needs to be deleted isolated
        if extrastuff not in self.node.extrainfo:
            return False

        #if theres something to replace it with, replace it and stop function
        if replacement != "":
          self.node.extrainfo.remove(extrastuff)
          self.node.extrainfo.append(replacement)
          return
        else:
          #no replacement just plain deletion
          if len(self.node.extrainfo) > 1:
            #multiple records of same key need to check if one that needs to be deleted is inside
            
            # remove that record from the list, preversing the node 
            self.node.extrainfo.remove(extrastuff)
          else:
            # proceeding to delete the node
            #finding the next node to delete
            nextnode = self
            parentkey = self.node.key
            if self.node.rightChild.node != None:
              
              nextnode = self.node.rightChild
              while(nextnode.node.leftChild.node is not None):
                #keep looping to get the smallest node in rightchild
                parentkey = nextnode.node.key
                nextnode = nextnode.node.leftChild
            # if self not the same as nextnode
            if self != nextnode:
              #copy the contents over
              self.node.key = nextnode.node.key
              self.node.extrainfo = nextnode.node.extrainfo
              #turning this node none, since its a leaf node anyway
              nextnode.node = nextnode.node.rightChild.node
            else:
              #the node that needs to be deleted has no rightchild, so just replace this node with its left child (shift leftchild up)
              self.node = nextnode.node.leftChild.node
            #return the key of the newnode's parent or deleted old nodes key 
            return parentkey
          
      elif self.node.key < key:
        #recursing
        return self.node.rightChild.deleteRecurse(key,extrastuff,replacement)
      else:
        #recursing
        return self.node.leftChild.deleteRecurse(key,extrastuff,replacement)
  
  def delete(self,key,extrastuff):
    # O(1) but its calls functions that are O(log2N)
    x = self.deleteRecurse(key,extrastuff)
    if x != False:
      #if node is deleted, search back for it and update all the nodes's tag,height and balance factor, do it if a change in node placing is detected
      if x != None:
        self.searchfix(x)
      return True
    else:
      return False
    
  def edit(self,key,extrastuff,replacement):
    # O(1) but its calls functions that are O(log2N)
    #check if the item to be replaced is found
    x = self.deleteRecurse(key,extrastuff,replacement)
    if x != False:      
      return True
    else:
      return False
        
  def searchfix(self,key):
    #time O(log2n)
    # recurse back to the node and updates its height and balance and rotate if needed
    if self.node != None:
      if self.node.key < key:
        self.node.rightChild.searchfix(key)
      elif self.node.key > key:
        self.node.leftChild.searchfix(key)
      self.calheight()
      self.setbfactor()
      
  def calheight(self):
    #time O(1)
    #calculates the new height of the node relative to children
    if self.node.leftChild.node != None and self.node.rightChild.node != None:
      self.height = max(self.node.leftChild.height,self.node.rightChild.height) + 1
      
    elif self.node.leftChild.node != None and self.node.rightChild.node == None:
      self.height = self.node.leftChild.height + 1
      self.setbfactor(0)
    elif self.node.leftChild.node == None and self.node.rightChild.node != None:
      self.height = self.node.rightChild.height + 1
    else:
      self.height = 1
      
  def countunderX(self,x):
    #time (O1) but it calls functions that are O(N) at worst
    # get the list of all the titles that are under x, uses the range: [lowest.value,x)
    counter = self.traversal(self.lowestvalue().key,x,True,False)
    if counter == None:
      counter = 0
    #returns length
    return len(counter)
  
  def listaboveY(self,y):
    #time (O1) but it calls functions that are O(N) at worst
    # get the list of all the titles that are above y, uses the range: (y,highestvalue()]
    thing = self.traversal(y, self.highestvalue().key,False,True)
    if thing == []:
      return None
    else:
      #returns the list
      return thing
  
  def getfromrange(self,a,b):
    #time (O1) but it calls functions that are O(N) at worst
    
    assert b>a, "2nd parameter must be larger than the 1st parameter" #make sure the range is proper
    # get the list of all the titles between a and b, uses the range: [a,b]
    var = self.traversal(a,b,True,True)
    if var == []:
      return None
    else:
      #return the list
      return var
  
  def descendprint(self):
    #time (O1) but it calls functions that are O(N)
    #return the list of every title in sorted descending order, uses the range: [lowestvalue(),highestvalue()]
    if self.node != None:
      return self.traversal(self.lowestvalue().key,self.highestvalue().key,True,True,True)
    else:
      return []

  def printTree(self): 
    # time O(logn) just to print trees out
    sVal = None
    if self.node:
        sVal = (self.node.leftChild.printTree(),(self.node.key,self.node.extrainfo,self.height,self.balancefactor,self.mytag),self.node.rightChild.printTree())
    return sVal
  
  def __str__(self):
    #time O1
    return str(self.printTree())
        

if __name__ == "__main__":
  
  #1 init()
  bst = AVLTree()

  for i in ["a","b","c","d","e","f","g","h","i"]:
    #2 insert()
    bst.insert(i,{i:1})
  
  #3 search()
  print(bst.search("a"))
  
  #4 getleft()
  print(bst.getLeft())
  
  #5 getright()
  print(bst.getRight())
  
  #6 getrootval()
  print(bst.getRootVal())

  #7 delete()
  print(bst.delete("d",{"d":1}))
  
  #8 highest value node's key
  print(bst.highestvalue().key)
  
  #9 lowest value
  print(bst.lowestvalue().key)

  #10 count under A
  print(bst.countunderX("d"))

  #11 display all stuff above threshold
  print(bst.listaboveY("d"))
  
  #12 display all within the range
  print(bst.getfromrange("a","e"))

  #13 print tree
  print(bst)
  
  #14 print in ascending order
  print(bst.ascendprint())

  #15 replacement function
  print(bst.edit("a",{"a":1},{"a":2}))
  

  

  

  



