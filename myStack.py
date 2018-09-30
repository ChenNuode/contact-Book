import ast
class Stack :
    def __init__(self,prelist=""):
        if prelist == "":
            self._theItems = list()
        else:
            self._theItems = ast.literal_eval(prelist)
        
    def isEmpty( self ):
        return len( self ) == 0
    
    def __len__ ( self ):
        return len( self._theItems )
    
    def peek( self ):
        assert not self.isEmpty(),"Cannot peek at an empty stack"
        return self._theItems[-1]
    
    def pop( self ):
        assert not self.isEmpty(),"Cannot pop from an empty stack"
        return self._theItems.pop()
    
    def push( self, item ):
        self._theItems.append( item )

    def __str__(self):
        return str(self._theItems)


if __name__ == "__main__":
    pass
    

