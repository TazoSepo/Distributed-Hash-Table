
# Let's start by implementing the Node of DHT, which will be a separate class
class Node:
    # constructor with the default values of successor and predecessor
    def __init__(self,id,next=None,previous=None):
        self.id = id

        # data property will store dictionary in which we can save the information for the node
        self.data = dict()
        # information about previous node
        self.previous = previous
        # property which will store the table of shortcuts
        self.Shortcuts = [next]
        self.finger = []

    # In order to keep shortcut table fresh and updated we need function for this
    def update_Shortcuts(self,dht,key):
        # deleting the old table entries from 1
        del self.Shortcuts[1:]
        # next, update the table and assign it to the property of node
        for k in range(1,key):
            self.Shortcuts.append(dht.find_node(dht.init_node,self.id+2**k))


# Now let's implement the class of dht itself
class DHT:
    def __init__(self,key):
        self.k = key

        # Size of the dht. the size would be 2 to the power of key size
        self.size=2**key
        # Arbitary starting node
        self.init_node = Node(0,key)
        # assign starting node to the shortcuts list (it should be the first element)
        self.init_node.Shortcuts[0]=self.init_node
        self.init_node.previous = self.init_node
        #Update shortcut list
        self.init_node.update_Shortcuts(self,key)

    #function for adding shortcuts
    def add_finger(self,node,target):
        node.finger.append(target)

    # function to list all of the nodes in the DHT
    def list(self):
        curr = self.init_node
        print(f"Node: {curr.id}:{[curr.finger[i] for i in range(len(curr.finger))]},S-{curr.Shortcuts[0].id},NS-{curr.Shortcuts[0].Shortcuts[0].id}")
        curr = curr.Shortcuts[0]
        while curr.id != self.init_node.id:
            print(f"Node: {curr.id}:{[curr.finger[i] for i in range(len(curr.finger))]},S-{curr.Shortcuts[0].id },NS-{curr.Shortcuts[0].Shortcuts[0].id}")
            curr = curr.Shortcuts[0]

    # We need the function to get the distance between two ID's 
    def ring_distance(self,x,y):
        # if the provided id's are the same then result is 0
        if x == y:
            return 0
        # if the first id is less then the second one, we return ditance of y - x
        elif x < y:
            return y - x
        # in case second id is greater, we return the whole size of the dht - sum of the id's
        else:
            return self.size - x + y
    
    # We also need hash function to retrieve the id
    def get_hash(self,key):
        # we have to return key.mod(k.size)
        return key % self.size

    # now let's implement function, which will help us find the node responsible of handling the provided key
    def find_node(self,init,key):
        # get the id from hash function
        hashed_id = self.get_hash(key)
        tmp = init
        while True:
            if tmp.id == hashed_id:
                return tmp
            if self.ring_distance(tmp.id,hashed_id) <= self.ring_distance(tmp.Shortcuts[0].id,hashed_id):
                return tmp.Shortcuts[0]
            table_size = len(tmp.Shortcuts)
            j = 0
            node_next = tmp.Shortcuts[-1]
            while j < table_size - 1:
                if self.ring_distance(tmp.Shortcuts[j].id, hashed_id) < self.ring_distance(tmp.Shortcuts[j+1].id,hashed_id):
                    node_next = tmp.Shortcuts[j]
                j = j + 1
            tmp = node_next   

    #Function to find and look up a key in the distributed hash table
    def lookup(self,init,key):
        # first find the node responsible for handling the key
        node_key = init
        # in other case we didn;t find any so return none
        counter = 0
        while True:
            if key in range(node_key.previous.id,node_key.id+1):
                break
            counter += 1
            node_key = node_key.Shortcuts[0]
        result = f"Result: Data stored in node {node_key.id} - {counter} requests sent"
        return result

    # Now let's see how we can add the new node to the dht (function join)
    def join(self,node_new):
        # find the exact not before which we have to put the new node
        node_main = self.find_node(self.init_node,node_new.id)
        # In case the node with the provided id already exists
        if node_main.id == node_new.id:
            print("That id already exists in the dht")
            return

        # now let's save the key-value pairs that are to be inserted in the new node
        for k in node_main.data:
            # get the id from has function
            hashed_id = self.get_hash(k)
            # if the distance between this hashed id and new node id is smaller than the 
            # distance of hashed_id and old node, then data of new node will be taken from old one
            if self.ring_distance(hashed_id,node_new.id) < self.ring_distance(hashed_id,node_main.id):
                node_new.data[k] = node_main.data[k]

        # after this we also have to update pointers of next and prevous noddes, cause the ne node is added
        node_previous = node_main.previous
        node_new.Shortcuts[0] = node_main
        # new node's previous node is node_previous
        node_new.previous = node_previous
        # Update main node
        node_main.previous = node_new
        # also update previous node's shortcuts
        node_previous.Shortcuts[0] = node_new
            
        # Next we want to setup the shortcuts for new node
        node_new.update_Shortcuts(self,self.k)

        # also let's delete the keys that were moved to the new added node
        for key in list(node_main.data.keys()):
            # get hashed id again
            hashed_id = self.get_hash(key)
            if self.ring_distance(hashed_id, node_new.id) < self.ring_distance(hashed_id, node_main.id):
                # delete the keys
                del node_main.data[key]
    
    # Function if we delete the node from the dht
    def leave(self,node):
        # copy every key=value pairs to it's successor
        for key, value in node.data.items():
            node.Shortcuts[0].data[key] = value
        
        # if after deletion there's no other node left
        if node.Shortcuts[0] == node:
            self.init_node=None
        else:
            # copy shortcut table to the previous node
            node.previous.Shortcuts[0] = node.Shortcuts[0]
            node.Shortcuts[0] = previous = node.previous

            # if the node that we have deleted was the entry point then we need to choose another one as an entry
            if self.init_node == node:
                self.init_node = node.Shortcuts[0]
        

    
    def Shortcut(self,node,short):
        node.finger.append(short)
        
    #Finally we need to have function to update shortcut tables for all of the nodes
    def update_all_shortcuts(self):
        self.init_node.update_Shortcuts(self,self.k)
        tmp = self.init_node.Shortcuts[0]
        while tmp != self.init_node:
            tmp.update_Shortcuts(self,self.k)
            tmp = tmp.Shortcuts[0]
            