import pickle


class Event:
    def to_message(self):
        return pickle.dumps(self)

    @staticmethod
    def from_message(msg):
        return pickle.loads(msg)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.__class__.__name__}: {str(vars(self))}'
