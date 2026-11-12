from collections import deque
from app.helpers import is_alive, bulk_list, NULL_ARRAY

class Waiters:
    def __init__(self):
        self.waiting = {} 

    def register(self, key, conn, deadline):
        self.waiting.setdefault(key, deque()).append((conn, deadline))

    def notify(self, key, item):
        queue = self.waiting.get(key)
        if queue:
            conn, _ = queue.popleft()
            conn.sendall(bulk_list([key, item]))
            return True
        return False


    def disconnect(self, conn):
        for key, queue in self.waiting.items():
            self.waiting[key] = deque(w for w in queue if w[0] != conn)


    def expire(self):
        for key, queue in self.waiting.items():
            alive = deque()

            for conn, deadline in queue:
                if is_alive(deadline):
                    alive.append((conn, deadline))
                else:
                    conn.sendall(NULL_ARRAY)

            self.waiting[key] = alive
