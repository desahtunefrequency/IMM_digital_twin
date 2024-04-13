import random

class IMM:
    def __init__(self):
        self.injection_time = 0.0
        self.cooling_time = 0.0
        self.demolding_time = 0.0
        self.cycle_count = 0
        self.machine_status = "Idle"
        self.power_consumption = 0.0

    def simulate(self):
        self.injection_time = random.uniform(0.38, 0.42)
        self.cooling_time = random.uniform(1.47, 1.53)
        self.demolding_time = random.uniform(4.95, 6.05)
        self.cycle_count += 1
        self.machine_status = "Running"
        self.power_consumption = random.uniform(10.0, 20.0)

    def reset(self):
        self.injection_time = 0.0
        self.cooling_time = 0.0
        self.demolding_time = 0.0
        self.machine_status = "Idle"
        self.power_consumption = 0.0
        