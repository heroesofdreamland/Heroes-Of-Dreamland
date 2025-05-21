class Order:
    def __init__(self, name: str, description: str, progress: int, cost: int):
        self.name = name
        self.description = description
        self.progress = progress
        self.cost = cost
        self.is_completed = False

    def update(self):
        pass

    def complete(self):
        pass