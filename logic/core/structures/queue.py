from collections import deque


class Queue:
    def __init__(self):
        self.__queue = deque()

    def reset(self):
        self.__queue.clear()

    def enqueue(self, item):
        self.__queue.append(item)

    def dequeue(self):
        return self.__queue.popleft()

    def is_empty(self):
        return not self.__queue
