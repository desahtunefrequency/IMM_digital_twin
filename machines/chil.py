import random

class CHIL:
    def __init__(self):
        self.delivery_temp_stationary = 0.0
        self.return_temp_stationary = 0.0
        self.pressure_stationary = 0.0
        self.delivery_temp_moving = 0.0
        self.return_temp_moving = 0.0
        self.pressure_moving = 0.0
        self.inlet_temp = 0.0
        self.outlet_temp = 0.0
        self.water_pressure = 0.0

    def simulate(self):
        self.delivery_temp_stationary = random.uniform(18.0, 22.0)
        self.return_temp_stationary = random.uniform(25.0, 30.0)
        self.pressure_stationary = random.uniform(1.0, 2.0)
        self.delivery_temp_moving = random.uniform(18.0, 22.0)
        self.return_temp_moving = random.uniform(25.0, 30.0)
        self.pressure_moving = random.uniform(1.0, 2.0)
        self.inlet_temp = random.uniform(15.0, 20.0)
        self.outlet_temp = random.uniform(25.0, 30.0)
        self.water_pressure = random.uniform(1.0, 3.0)