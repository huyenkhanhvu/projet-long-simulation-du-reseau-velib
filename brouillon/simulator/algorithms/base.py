class RoutingAlgorithm:
    def __init__(self):
        self.router = None

    def process_messages(self, messages):
        raise NotImplementedError

    def create_messages(self):
        raise NotImplementedError
