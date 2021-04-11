# Distributed-Hash-Table
DHT implementation with python (cause why not).

There are several command you can run:

1. **List**: List the nodes in the ring (sorted from lower to higher). It also shows the references that
each node is storing

2. **Lookup**: It is used to lookup for a node containing a particular key. The lookup also defines the
node that receives the lookup request. If just a key value is passed, then the lookup starts from
the node with the lowest value. A node lookup for key data to itself has a weight of zero. A node
lookup for key data to its finger table (shortcuts) or another node has a weight of 1. Lookups are
accumulated until the key value is found

3. **Join**: this commands allows a new node to join the ring. Notice that successor and next successor
references should be updated

4. **Leave**: this commands allows a node to leave the ring. We will handle the simple resilience case
in which a single node leaves at the time. Leave cannot be applied when there is just a single
node remaining

5. **Shortcut**: this command adds a shortcut from one node to another

6. **Remove**: This command removes the nodes from the ring.

**launching Manual**: just compile the main.py file. ezpz :)
