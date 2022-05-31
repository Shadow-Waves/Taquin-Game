class Queue:
    def __init__(self,*args):
        self.queue = list(args)
        
    def append(self,element):
        self.queue.append(element)
        
    def is_empty(self):
        return len(self.queue) == 0
        
    def pop(self):
        assert not self.is_empty(),"empty queue"
        return self.queue.pop(0)
        
    def first(self):
        return self.pop()
        
    def size(self):
        return len(self.queue)