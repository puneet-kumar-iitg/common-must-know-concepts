import time
from functools import wraps
from typing import Any

class Node:

    def __init__(self, key: str = None, val: Any = 0, next : Any = None, prev : Any = None):
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev


class LRUCache:
    '''Build a key value store with given capacity and should have below time constraints'''

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.store = {}
        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    def __iter__(self):
        curr = self.head.next
        while curr != self.tail:
            yield curr.key
            curr = curr.next


    def __len__(self):
        return len(self.store)

    def get(self, key: str):
        if key not in self.store.keys():
            return None
        node = self.store.get(key)
        self.move_node_to_head(node)
        return node.val
    
    def deattach_node(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node
        return node
    
    def move_node_to_head(self, node : Node):
        self.deattach_node(node)
        self.add_node_to_head(node)
        

    def add_node_to_head(self, node):
        head_next = self.head.next
        self.head.next = node
        node.next = head_next
        head_next.prev = node
        node.prev = self.head


    def push(self, key: str, val: Any):
        # add new node if unavailable
        # update existing node
        # check cache capacity for eviction

        if key in self.store.keys():
            old_node = self.store.get(key)
            old_node.val = val
            self.move_node_to_head(old_node)
        else:
            if len(self.store.keys()) == self.capacity:
                lru_node = self.tail.prev
                self.deattach_node(lru_node)
                lru_key = lru_node.key
                self.store.pop(lru_key)
            new_node = Node(key, val)
            self.add_node_to_head(new_node)
            self.store[key] = new_node


cache = LRUCache(capacity=100)


def ttl_cache(ttl_seconds: int):

    def decorator(func):
        # store cached results: {arguments: (result, expiration_timestamp)}
        # cache = {}

        @wraps(func) # decorator from functools that preserves metadata of function e.g. __name__, __doc__, __wrap__
        def wrapper(*args):
            current_time = time.time()

            # 1. Check if the result is in the cache AND hasn't expired yet
            if cache.get(args[0]):
                result, expiry_time = cache.get(args[0])
                if current_time < expiry_time:
                    print(f"[CACHE HIT] Returning saved result for {args}")
                    return result
                else:
                    print(f"[CACHE EXPIRED] Fetching fresh data for {args}...")

            # 2. If not cached or expired, run the actual slow function
            result = func(*args)
            
            # 3. Save the new result with its future expiration timestamp
            cache.push(args[0],(result, current_time + ttl_seconds))
            return result

        return wrapper
    return decorator


@ttl_cache(ttl_seconds=5)
def greetings(name: str, msg: str = ""):
    default = "Welcome to decorator world."
    greet = f"Hi {name}, {msg or default}"
    return greet

        

if __name__ == "__main__":
    name = "Tester"
    msg = "How is your AI concepts knowledge?"
    # after decorator : testing function
    # print(greetings(name, msg))
    print(len(cache))
    print(greetings(name, msg))
    print(len(cache))
