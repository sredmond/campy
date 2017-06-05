import random

"""TODO: singleton?"""
class RandomGenerator(random.Random):

    def __init__(self):


    def randint(self, low=0, high=10):
        pass

    def randBoolean(self, prob=0.5):
        pass

    def nextDouble(self, low=0, high=1):
        return low + (high - low) * self.random()

    def nextColor(self):
        pass
