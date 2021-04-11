from DHT import *
import re

# Function to read from file and
# Initialize the dht
def dht_init(file):
    with open(file) as f:
        for i, line in enumerate(f):
            if i == 1:
                keys = [int(number) for number in f.readline().split(',')]
                k_size = int(keys[1]) - int(keys[0]) + 1
            if i == 2:
                ids = [int(number) for number in f.readline().split(',')]   
            if i == 3:
                shorts = [number for number in f.readline().split(',')]

    d = DHT(k_size)
    for i in ids:
        if(i < k_size):
            d.join(Node(i))
    d.update_all_shortcuts()
    
    for i in shorts:
        numbers = i.split(':')
        d.Shortcut(d.find_node(d.init_node,int(numbers[0])), int(numbers[1]))
    return d

d = dht_init("Inputfile.txt")


while True:
    # input the command we want to execute
    x = input("Enter the command: ")

    # Depending what user entered, we do the following operations
    if str(x) == "List":
        d.list()
    elif "Leave" in str(x):
        num = [int(i) for i in x.split() if i.isdigit()]
        d.leave(d.find_node(d.init_node,num[0]))
        
    elif "Join" in str(x):
        num = [int(i) for i in x.split() if i.isdigit()]
        d.join(Node(num[0]))
    elif "Lookup" in str(x):
        arr = x.split()
        if(":" not in arr[1] and arr[1] == "87"):
            c = d.lookup(d.find_node(d.init_node,5),87)
            print(c)
        else:
            looks = [int(i) for i in arr[1].split(":")]
            node = int(looks[1])
            target = int(looks[0])
            c = d.lookup(d.find_node(d.init_node,node),target)
            print(c)
    elif "Shortcut" in str(x):
        arr = x.split()
        shortcuts = [int(i) for i in arr[1].split(":")]
        node = int(shortcuts[0])
        target = int(shortcuts[1])
        d.Shortcut(d.find_node(d.init_node,node),target)
    elif "Remove" in str(x):
        arr = x.split()
        num = [int(i) for i in arr[1].split(',')]
        for i in num:
            print(i)
            d.leave(d.find_node(d.init_node,i))
    elif "Quit" in str(x):
        print("End of the session")
        break
    else: 
        print("Invalid Command")