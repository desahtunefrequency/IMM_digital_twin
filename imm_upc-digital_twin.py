import time
import random
from opcua import Server, ua
import sqlite3
from machines.imm import IMM
from machines.iml import IML
from machines.chil import CHIL
from machines.m_con import M_CON
from machines.c_disp import C_DISP
from machines.robo import ROBO


# Set up the OPC UA server
server = Server()
url = "opc.tcp://localhost:4840"
server.set_endpoint(url)

# Connect to the SQLite database
connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# Fetch the equipment data from the database
cursor.execute("SELECT * FROM main.Equipment")
equipment_data = cursor.fetchall()

# Create equipment objects and add them to the OPC UA address space
equipment_objects = {}

for row in equipment_data:
    equipment_id = row[0]
    group = row[1]
    equipment_type = row[4]

    device_name = f"{group}_{equipment_type}_{equipment_id}"
    device_name_2 = f"{group}_{equipment_type}_{equipment_id}"
    print(device_name_2)

    if equipment_type == "IMM":
        equipment = IMM()
    elif equipment_type == "IML":
        equipment = IML()
    elif equipment_type == "CHIL":
        equipment = CHIL()
    elif equipment_type == "C_DISP":
        equipment = C_DISP()
    elif equipment_type == "M_CON":
        equipment = M_CON()
    elif equipment_type == "ROBO":
        equipment = ROBO()
    else:
        continue

    equipment_node = server.nodes.objects.add_object(
        ua.NodeId(f"ns=2;s={device_name}"), device_name
    )

    if equipment_type == "IMM":
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=InjectionTime_{device_name}"), "InjectionTime", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=CoolingTime_{device_name}"), "CoolingTime", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=DemoldingTime_{device_name}"), "DemoldingTime", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=CycleCount_{device_name}"), "CycleCount", 0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=MachineStatus_{device_name}"), "MachineStatus", "Idle"
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=PowerConsumption_{device_name}"), "PowerConsumption", 0.0
        )
    elif equipment_type == "IML":
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=LabelingState_{device_name}"), "LabelingState", False
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=RobotCycleTime_{device_name}"), "RobotCycleTime", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=LabelMagazineState_{device_name}"),
            "LabelMagazineState",
            100.0,
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=EnergyConsumption_{device_name}"),
            "EnergyConsumption",
            0.0,
        )
    elif equipment_type == "CHIL":
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=DeliveryTempStationary_{device_name}"),
            "DeliveryTempStationary",
            0.0,
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=ReturnTempStationary_{device_name}"),
            "ReturnTempStationary",
            0.0,
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=PressureStationary_{device_name}"),
            "PressureStationary",
            0.0,
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=DeliveryTempMoving_{device_name}"),
            "DeliveryTempMoving",
            0.0,
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=ReturnTempMoving_{device_name}"), "ReturnTempMoving", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=PressureMoving_{device_name}"), "PressureMoving", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=InletTemp_{device_name}"), "InletTemp", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=OutletTemp_{device_name}"), "OutletTemp", 0.0
        )
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=WaterPressure_{device_name}"), "WaterPressure", 0.0
        )
    elif equipment_type == "C_DISP":
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=CycleTime_{device_name}"), "CycleTime", 0.0
        )
    elif equipment_type == "M_CON":
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=WorkingTime_{device_name}"), "WorkingTime", 0.0
        )
    elif equipment_type == "ROBO":
        equipment_node.add_variable(
            ua.NodeId(f"ns=2;s=CycleTime_{device_name}"), "CycleTime", 0.0
        )

    equipment_objects[device_name] = equipment

# Start the OPC UA server
server.start()

try:
    while True:
        # Simulate the behavior of each equipment
        for device_name, equipment in equipment_objects.items():
            equipment.simulate()

            if isinstance(equipment, IMM):
                injection_time_node = server.get_node(
                    ua.NodeId(f"ns=2;s=InjectionTime_{device_name}")
                )
                if injection_time_node:
                    injection_time_node.set_value(equipment.injection_time)

                cooling_time_node = server.get_node(
                    ua.NodeId(f"ns=2;s=CoolingTime_{device_name}")
                )
                if cooling_time_node:
                    cooling_time_node.set_value(equipment.cooling_time)

                demolding_time_node = server.get_node(
                    ua.NodeId(f"ns=2;s=DemoldingTime_{device_name}")
                )
                if demolding_time_node:
                    demolding_time_node.set_value(equipment.demolding_time)

                cycle_count_node = server.get_node(
                    ua.NodeId(f"ns=2;s=CycleCount_{device_name}")
                )
                if cycle_count_node:
                    cycle_count_node.set_value(equipment.cycle_count)

                machine_status_node = server.get_node(
                    ua.NodeId(f"ns=2;s=MachineStatus_{device_name}")
                )
                if machine_status_node:
                    machine_status_node.set_value(equipment.machine_status)

                power_consumption_node = server.get_node(
                    ua.NodeId(f"ns=2;s=PowerConsumption_{device_name}")
                )
                if power_consumption_node:
                    power_consumption_node.set_value(equipment.power_consumption)

            elif isinstance(equipment, IML):
                labeling_state_node = server.get_node(
                    ua.NodeId(f"ns=2;s=LabelingState_{device_name}")
                )
                if labeling_state_node:
                    labeling_state_node.set_value(equipment.labeling_state)

                robot_cycle_time_node = server.get_node(
                    ua.NodeId(f"ns=2;s=RobotCycleTime_{device_name}")
                )
                if robot_cycle_time_node:
                    robot_cycle_time_node.set_value(equipment.robot_cycle_time)

                label_magazine_state_node = server.get_node(
                    ua.NodeId(f"ns=2;s=LabelMagazineState_{device_name}")
                )
                if label_magazine_state_node:
                    label_magazine_state_node.set_value(equipment.label_magazine_state)

                energy_consumption_node = server.get_node(
                    ua.NodeId(f"ns=2;s=EnergyConsumption_{device_name}")
                )
                if energy_consumption_node:
                    energy_consumption_node.set_value(equipment.energy_consumption)

            elif isinstance(equipment, CHIL):
                delivery_temp_stationary_node = server.get_node(
                    ua.NodeId(f"ns=2;s=DeliveryTempStationary_{device_name}")
                )
                if delivery_temp_stationary_node:
                    delivery_temp_stationary_node.set_value(
                        equipment.delivery_temp_stationary
                    )

                return_temp_stationary_node = server.get_node(
                    ua.NodeId(f"ns=2;s=ReturnTempStationary_{device_name}")
                )
                if return_temp_stationary_node:
                    return_temp_stationary_node.set_value(
                        equipment.return_temp_stationary
                    )

                pressure_stationary_node = server.get_node(
                    ua.NodeId(f"ns=2;s=PressureStationary_{device_name}")
                )
                if pressure_stationary_node:
                    pressure_stationary_node.set_value(equipment.pressure_stationary)

                delivery_temp_moving_node = server.get_node(
                    ua.NodeId(f"ns=2;s=DeliveryTempMoving_{device_name}")
                )
                if delivery_temp_moving_node:
                    delivery_temp_moving_node.set_value(equipment.delivery_temp_moving)

                return_temp_moving_node = server.get_node(
                    ua.NodeId(f"ns=2;s=ReturnTempMoving_{device_name}")
                )
                if return_temp_moving_node:
                    return_temp_moving_node.set_value(equipment.return_temp_moving)

                pressure_moving_node = server.get_node(
                    ua.NodeId(f"ns=2;s=PressureMoving_{device_name}")
                )
                if pressure_moving_node:
                    pressure_moving_node.set_value(equipment.pressure_moving)

                inlet_temp_node = server.get_node(
                    ua.NodeId(f"ns=2;s=InletTemp_{device_name}")
                )
                if inlet_temp_node:
                    inlet_temp_node.set_value(equipment.inlet_temp)

                outlet_temp_node = server.get_node(
                    ua.NodeId(f"ns=2;s=OutletTemp_{device_name}")
                )
                if outlet_temp_node:
                    outlet_temp_node.set_value(equipment.outlet_temp)

                water_pressure_node = server.get_node(
                    ua.NodeId(f"ns=2;s=WaterPressure_{device_name}")
                )
                if water_pressure_node:
                    water_pressure_node.set_value(equipment.water_pressure)

            elif isinstance(equipment, C_DISP):
                cycle_time_node = server.get_node(
                    ua.NodeId(f"ns=2;s=CycleTime_{device_name}")
                )
                if cycle_time_node:
                    cycle_time_node.set_value(equipment.cycle_time)

            elif isinstance(equipment, M_CON):
                working_time_node = server.get_node(
                    ua.NodeId(f"ns=2;s=WorkingTime_{device_name}")
                )
                if working_time_node:
                    working_time_node.set_value(equipment.working_time)

            elif isinstance(equipment, ROBO):
                cycle_time_node = server.get_node(
                    ua.NodeId(f"ns=2;s=CycleTime_{device_name}")
                )
                if cycle_time_node:
                    cycle_time_node.set_value(equipment.cycle_time)

        # Wait for a specific interval before the next simulation step
        time.sleep(10.0)  # Adjust the interval as needed

except KeyboardInterrupt:
    # Stop the OPC UA server when the simulation is interrupted
    server.stop()
    connection.close()
