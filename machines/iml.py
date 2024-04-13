import random

class IML:
    def __init__(self):
        self.labeling_state = False
        self.robot_cycle_time = 0.0
        self.label_magazine_state = 100.0
        self.energy_consumption = 0.0

    def simulate(self):
        self.labeling_state = random.choice([True, False])
        self.robot_cycle_time = random.uniform(2.0, 5.0)
        self.label_magazine_state = max(
            0.0, self.label_magazine_state - random.uniform(0.5, 1.5)
        )
        self.energy_consumption = random.uniform(1.0, 5.0)