class Node:
    def __init__(self,r,p,q):
        self.r=r
        self.p=p
        self.q=q
    


class PriorityQueue:
    def __init__(self,ismax:bool):
        self.queue=[]
        self.ismax=ismax

    def isEmpty(self):
        return (len(self.queue) == 0)
    
    def insert(self,node:Node):
        if (self.ismax):
            index=len(self.queue)
            for i in range(0,len(self.queue)): # uszeregowanie po q
                if node.q>self.queue[i].q:
                    index=i
                    break
        else:
            index=len(self.queue)
            for i in range(0,len(self.queue)): # uszeregowanie po r
                if node.r<self.queue[i].r:
                    index=i
                    break
        self.queue.insert(index,node)

    def pop(self):
        return self.queue.pop(0)