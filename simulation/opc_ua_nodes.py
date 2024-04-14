from opcua import Server, ua
import sqlite3


def add_opc_ua_nodes(server, equipment_node, equipment_id, device_name):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    print(
        f"opc.py, equipment_id: {equipment_id}, device_name: {device_name}: equipmnet node: {equipment_node}"
    )

    # Fetch parameter names and values from the simulation_settings table for the specific equipment
    cursor.execute(
        "SELECT parameter_name, value FROM simulation_settings WHERE equipment_id=?",
        (equipment_id,),
    )
    parameter_data = cursor.fetchall()
    print(f"opc.py, parameters_data for {device_name}: {parameter_data}")
    conn.close()

    # Create OPC UA nodes dynamically for each parameter
    for parameter_name, value in parameter_data:
        node_id = ua.NodeId(f"ns=2;s={parameter_name}_{device_name}")
        print("opc.py, node_id", node_id)
        parameter_node = equipment_node.add_variable(node_id, parameter_name, value)
        parameter_node.set_writable()
