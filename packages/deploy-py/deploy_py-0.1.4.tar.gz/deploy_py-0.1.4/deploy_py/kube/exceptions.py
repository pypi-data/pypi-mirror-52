class PodNotFoundError(Exception):
    def __init__(self, selectors):
        self.message = f"no pods match given selectors: {selectors}"
