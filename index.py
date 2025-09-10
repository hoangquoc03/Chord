import hashlib
import random


def hash_key(key, m=8):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2 ** m)


class Node:
    def __init__(self, node_id, m=8):
        self.id = node_id
        self.m = m
        self.successor = self
        self.predecessor = None

    def __repr__(self):
        return f"Node({self.id})"

    def join(self, known_node):

        if known_node:
            self.init_finger_table(known_node)
        else:
            self.successor = self

    def init_finger_table(self, known_node):
        self.successor = known_node.find_successor(self.id)

    def find_successor(self, key_id):

        if self == self.successor:
            return self
        if self.id < key_id <= self.successor.id or (
            self.id > self.successor.id and (key_id > self.id or key_id <= self.successor.id)
        ):
            return self.successor
        else:
            return self.successor.find_successor(key_id)

    def stabilize(self):

        x = self.successor.predecessor
        if x and self.id < x.id < self.successor.id:
            self.successor = x
        self.successor.notify(self)

    def notify(self, node):
        if not self.predecessor or (self.predecessor.id < node.id < self.id):
            self.predecessor = node


class ChordRing:
    def __init__(self, m=8):
        self.m = m
        self.nodes = []

    def add_node(self, key):

        node_id = hash_key(str(key), self.m)
        new_node = Node(node_id, self.m)

        if not self.nodes:
            new_node.join(None)
        else:
            known_node = random.choice(self.nodes)
            new_node.join(known_node)
            for n in self.nodes:
                n.stabilize()
            new_node.stabilize()

        self.nodes.append(new_node)
        return new_node

    def find_node(self, key):

        if not self.nodes:
            return None
        key_id = hash_key(str(key), self.m)
        return self.nodes[0].find_successor(key_id)


def test():
    ring = ChordRing(m=5) 

    n1 = ring.add_node("10")  
    n2 = ring.add_node("20")   
    n3 = ring.add_node("30") 

    print("Danh sách node trong hệ thống:")
    for node in sorted(ring.nodes, key=lambda x: x.id):
        print(f" - {node}")

    keys = ["apple", "banana", "cherry"]

    print("\nPhân phối key:")
    for k in keys:
        node = ring.find_node(k)
        print(f" Key '{k}' (hash={hash_key(k, 5)}) -> {node}")



if __name__ == "__main__":
    test()
