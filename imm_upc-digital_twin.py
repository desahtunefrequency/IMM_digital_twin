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
from simulation.create import create_equipment
from simulation.opc_ua_nodes import add_opc_ua_nodes
from simulation.update_nodes import *


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

    equipment = create_equipment(equipment_type, device_name)
    if equipment is None:
        continue

    equipment_node = server.nodes.objects.add_object(
        ua.NodeId(f"ns=2;s={device_name}"), device_name
    )
    add_opc_ua_nodes(server, equipment_node, equipment_type, device_name)

    equipment_objects[device_name] = equipment


# Start the OPC UA server
server.start()
try:
    while True:
        # Simulate the behavior of each equipment
        for device_name, equipment in equipment_objects.items():
            equipment.simulate()

            # Update nodes based on equipment type
            if isinstance(equipment, IMM):
                update_imm_nodes(server, equipment, device_name)
            elif isinstance(equipment, IML):
                update_iml_nodes(server, equipment, device_name)
            elif isinstance(equipment, CHIL):
                update_chil_nodes(server, equipment, device_name)
            elif isinstance(equipment, C_DISP):
                update_c_disp_nodes(server, equipment, device_name)
            elif isinstance(equipment, M_CON):
                update_m_con_nodes(server, equipment, device_name)
            elif isinstance(equipment, ROBO):
                update_robo_nodes(server, equipment, device_name)

        time.sleep(10.0)  # Adjust the interval as needed

except KeyboardInterrupt:
    # Stop the OPC UA server when the simulation is interrupted
    server.stop()
    connection.close()
