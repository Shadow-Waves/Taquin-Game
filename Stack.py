class Stack:
    def __init__(self,*args):
        self.stack = list(args)
        
    def append(self,element):
        self.stack.append(element)
        
    def is_empty(self):
        return len(self.stack) == 0
        
    def pop(self):
        assert not self.is_empty(),"empty stack"
        return self.stack.pop()
        
    def last(self):
        return self.pop()
        
    def size(self):
        return len(self.stack)