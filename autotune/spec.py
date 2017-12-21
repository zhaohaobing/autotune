from numpy import random
import json


class Spec:

    @classmethod
    def load(cls, fname):
        config = {}
        with open(fname) as f:
            for k, v in json.load(f).items():
                if isinstance(v, list):
                    if isinstance(v[0], int):
                        config[k] = IntRange(*v)
                    else:
                        assert isinstance(v[0], float)
                        config[k] = FloatRange(*v)
                else:
                    assert 'Unsupported {}={}'.format(k, v)
        return config


class Range(Spec):
    
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def sample(self):
        raise NotImplementedError()

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.low, self.high)


class IntRange(Range):

    def sample(self):
        return random.randint(self.low, self.high)


class FloatRange(Range):

    def sample(self):
        return random.uniform(self.low, self.high)
