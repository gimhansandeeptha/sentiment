import asyncio

class SentimentData:
    def __init__(self) -> None:
        self.cases = None
        self.lock = asyncio.Lock()

    def load_data(self, cases:list) -> None:
        if self.cases is None:
            self.cases = cases
