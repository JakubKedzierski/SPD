import numpy as np

class MaxHeap:
    tab = None
    heap_size = 0

    def heapify_max_q_in_node(self,n,id):
        idhelp = id
        left = 2 * id + 1
        right = 2 * id + 2

        if (left < n) and (self.tab[left][3] > self.tab[idhelp][3]):
            idhelp=left
        else:
            idhelp=id

        if (right < n) and (self.tab[right][3] > self.tab[idhelp][3]):
            idhelp = right

        if (idhelp != id):

            self.tab[[id,idhelp]] = self.tab[[idhelp,id]]
            self.heapify_max_q_in_node(n, idhelp)


    def parent(self, index):
        return int( (index-1)/2 )


    def insert_max_heap(self, row):
        self.heap_size = self.heap_size + 1

        if self.heap_size == 1:
            self.tab = np.zeros((1, 4))
            self.tab[0, 0] = row[0]
            self.tab[0, 1] = row[1]
            self.tab[0, 2] = row[2]
            self.tab[0, 3] = row[3]
            return

        self.tab = np.vstack((self.tab, row))
        index = self.heap_size - 1

        while index != 0 and (self.tab[self.parent(index)][3] < self.tab[index][3]):
            self.tab[[index, self.parent(index)]] = self.tab[[self.parent(index), index]]
            index = int((index-1)/2)


    def build_heap_max_q_in_node(self,n):
        startId = int(n/2-1)
        for i in range(startId,-1,-1):
            self.heapify_max_q_in_node(n,i)
        self.heap_size=np.shape(self.tab)[0]


    def pop_max(self):
        if self.heap_size <= 0:
            return np.iinfo(np.int32).min

        if self.heap_size == 1:
            self.heap_size =self.heap_size-1
            root=np.copy(self.tab[0])
            self.tab=np.delete(self.tab,0,axis=0)
            return root

        root = np.copy(self.tab[0])
        self.tab[0] = np.copy(self.tab[self.heap_size - 1])
        self.tab=np.delete(self.tab,self.heap_size-1,axis=0)
        self.heap_size = self.heap_size-1
        self.heapify_max_q_in_node(self.heap_size,0)
        return root

    def isEmpty(self):
        if self.heap_size<=0:
            return True
        else:
            return False

class MinHeap():
    tab = None
    heap_size = 0

    def parent(self, index):
        return int( (index-1)/2 )

    def insert_min_heap(self, row):
        self.heap_size = self.heap_size + 1

        if self.heap_size == 1:
            self.tab = np.zeros((1, 4))
            self.tab[0, 0] = row[0]
            self.tab[0, 1] = row[1]
            self.tab[0, 2] = row[2]
            self.tab[0, 3] = row[3]
            return

        self.tab = np.vstack((self.tab, row))
        index = self.heap_size - 1

        while index != 0 and (self.tab[self.parent(index)][1] > self.tab[index][1]):
            self.tab[[index, self.parent(index)]] = self.tab[[self.parent(index), index]]
            index = int((index-1)/2)

    def heapify_min_r_in_node(self,n,id):
        idhelp = id
        left = 2 * id + 1
        right = 2 * id + 2

        if (left < n) and (self.tab[left][1] < self.tab[idhelp][1]):
            idhelp=left
        else:
            idhelp=id

        if (right < n) and (self.tab[right][1] < self.tab[idhelp][1]):
            idhelp = right

        if (idhelp != id):

            self.tab[[id,idhelp]] = self.tab[[idhelp,id]]
            self.heapify_min_r_in_node(n, idhelp)


    def build_heap_min_r_in_node(self,n):
        startId = int(n/2-1)
        for i in range(startId,-1,-1):
            self.heapify_min_r_in_node(n,i)
        self.heap_size=np.shape(self.tab)[0]


    def pop_min(self):
        if self.heap_size <= 0:
            return np.iinfo(np.int32).min

        if self.heap_size == 1:
            self.heap_size =self.heap_size-1
            root=np.copy(self.tab[0])
            self.tab=np.delete(self.tab,0,axis=0)
            return root

        root = np.copy(self.tab[0])
        self.tab[0] = np.copy(self.tab[self.heap_size - 1])
        self.tab=np.delete(self.tab,self.heap_size-1,axis=0)
        self.heap_size = self.heap_size-1
        self.heapify_min_r_in_node(self.heap_size,0)
        return root


    def isEmpty(self):
        if self.heap_size<=0:
            return True
        else:
            return False


