import random

class M_CON:
    def __init__(self):
        self.working_time = 0.0

    def simulate(self):
        self.working_time = random.uniform(1.0, 2.0)