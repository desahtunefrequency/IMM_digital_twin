import time
from opcua import Server, ua
import sqlite3
from machines.equipment import Equipment
from simulation.opc_ua_nodes import add_opc_ua_nodes
from simulation.update_nodes import update_nodes


# Set up the OPC UA server
server = Server()
url = "opc.tcp://localhost:4840"
server.set_endpoint(url)

# Connect to the SQLite database
connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# Fetch equipment IDs from simulation_settings table
cursor.execute("SELECT DISTINCT equipment_id FROM simulation_settings")
equipment_ids = [row[0] for row in cursor.fetchall()]

print(equipment_ids)


# Create equipment objects and add them to the OPC UA address space
equipment_objects = {}
for equipment_id in equipment_ids:
    # Fetch equipment details from the equipment table
    cursor.execute("SELECT * FROM equipment WHERE SAP=?", (equipment_id,))
    equipment_data = cursor.fetchone()

    if not equipment_data:
        print(f"Alert: Equipment with SAP {equipment_id} not found in equipment table")
        continue

    group, equipment_type = equipment_data[1], equipment_data[4]
    device_name = f"{group}_{equipment_type}_{equipment_id}"
    print(device_name)

    equipment = Equipment(equipment_id, server, group, equipment_type)

    equipment_node = server.nodes.objects.add_object(
        ua.NodeId(f"ns=2;s={device_name}"), device_name
    )
    add_opc_ua_nodes(server, equipment_node, equipment_id, device_name)
    equipment_objects[device_name] = equipment

# Start the OPC UA server
server.start()

try:
    while True:
        # Simulate the behavior of each equipment
        for device_name, equipment in equipment_objects.items():
            equipment.simulate()

        time.sleep(100.0)  # Adjust the interval as needed

except KeyboardInterrupt:
    # Stop the OPC UA server when the simulation is interrupted
    server.stop()
    connection.close()
