from firestorm.db.schema import Schema


class Session:
    def __init__(self):
        self.schema = Schema()
