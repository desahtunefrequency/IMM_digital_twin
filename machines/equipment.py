import time
import random
import sqlite3
from simulation.update_nodes import update_nodes


class Equipment:
    def __init__(self, equipment_id, server, group, equipment_type):
        self.equipment_id = equipment_id
        self.server = server
        self.group = group
        self.equipment_type = equipment_type
        self.parameters = self._load_simulation_settings()
        self.cycle_count = 0
        self.status = "Idle"

    def _load_simulation_settings(self):
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT setting_id, parameter_name, value, deviation_type, deviation_value, target_parameter, formula, count_cycle FROM simulation_settings WHERE equipment_id=?",
            (self.equipment_id,),
        )
        settings_data = cursor.fetchall()
        conn.close()

        parameters = {}
        for row in settings_data:
            parameter_name = row[1]
            target_parameter = row[5]
            parameters[parameter_name] = {
                "setting_id": row[0],
                "value": float(row[2]),
                "deviation_type": row[3],
                "deviation_value": float(row[4]),
                "target_parameter": target_parameter,
                "formula": row[6],
                "count_cycle": row[7],
            }
            if target_parameter and target_parameter not in parameters:
                parameters[target_parameter] = {
                    "setting_id": None,
                    "value": None,
                    "deviation_type": None,
                    "deviation_value": None,
                    "target_parameter": None,
                    "formula": None,
                    "count_cycle": None,
                }

        return parameters

    def _get_parameter_value(self, parameter_name):
        parameter_data = self.parameters[parameter_name]
        nominal_value = parameter_data["value"]
        deviation_type = parameter_data["deviation_type"]
        deviation_value = parameter_data["deviation_value"]
        print("equipment.py, nominal_value: ", nominal_value)
        print("equipment.py, deviation_type: ", deviation_type)
        print("equipment.py, deviation_value: ", deviation_value)

        if nominal_value is None or deviation_value is None or deviation_type is None:
            return nominal_value

        if deviation_type == "percentage":
            deviation = nominal_value * (deviation_value / 100) * random.uniform(-1, 1)
        else:  # absolute deviation
            deviation = deviation_value * random.uniform(-1, 1)

        simulated_value = nominal_value + deviation
        print(f"Simulated value for {parameter_name}: {simulated_value}")
        return simulated_value

    def simulate(self):
        while True:
            # Reload the simulation settings from the database
            self.parameters = self._load_simulation_settings()

            print(
                f"Simulating device: {self.group}_{self.equipment_type}_{self.equipment_id}"
            )

            for parameter_name, parameter_data in self.parameters.items():
                target_parameter = parameter_data["target_parameter"]
                formula = parameter_data["formula"]
                count_cycle = parameter_data["count_cycle"]

                print(f"Processing parameter: {parameter_name}")

                if count_cycle == 1:
                    # Calculate the parameter value with deviations
                    value = self._get_parameter_value(parameter_name)
                    self.parameters[parameter_name]["value"] = value

                    if target_parameter and formula:
                        # Evaluate the formula using the current parameter values
                        formula = formula.replace('"""', '"')
                        for param_name in self.parameters:
                            if param_name in formula:
                                param_value = self.parameters[param_name]["value"]
                                if param_value is None:
                                    formula = None
                                    break
                                formula = formula.replace(param_name, str(param_value))
                        if formula:
                            try:
                                calculated_value = eval(formula)
                                self.parameters[target_parameter][
                                    "value"
                                ] = calculated_value
                            except (KeyError, TypeError, NameError, ZeroDivisionError):
                                pass  # Skip updating the target parameter if an error occurs

            # Update the OPC UA nodes with the new parameter values
            update_nodes(self.server, self)

            self.cycle_count += 1
            self.status = "Running"

            # Print the simulated values for each parameter
            print(
                f"Simulated values for {self.group}_{self.equipment_type}_{self.equipment_id}:"
            )
            for parameter_name, parameter_data in self.parameters.items():
                print(f"{parameter_name}: {parameter_data['value']}")

            # Wait for a specific interval before the next simulation cycle
            time.sleep(5)  # Adjust the interval as needed

    def update_setting(self, parameter_name, new_value):
        print("equipment.py, parameter_name: ", parameter_name)
        print("equipment.py, new_value: ", new_value)

        if parameter_name in self.parameters:
            self.parameters[parameter_name]["value"] = new_value
            update_nodes(self.server, self)

            # Update the corresponding value in the database
            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE simulation_settings SET value = ? WHERE equipment_id = ? AND parameter_name = ?",
                (new_value, self.equipment_id, parameter_name),
            )
            conn.commit()
            conn.close()

    def reset(self):
        self.cycle_count = 0
        self.status = "Idle"
