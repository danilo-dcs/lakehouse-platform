from hashlib import md5

class HashHandler:

    def __init__(self) -> None:
        self.md5_hash = md5()

    def encode(self, word: str) -> str:
        self.md5_hash.update(word.encode('utf-8'))
        return self.md5_hash.hexdigest()