import heapq


class PriorityQueue:
    def __init__(self):
        self.__heap = []

    def reset(self):
        self.__heap.clear()

    def enqueue(self, item):
        heapq.heappush(self.__heap, item)

    def dequeue(self):
        return heapq.heappop(self.__heap)

    def is_empty(self):
        return not self.__heap
