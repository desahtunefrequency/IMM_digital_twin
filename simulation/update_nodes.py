from opcua import ua


def update_nodes(server, equipment):
    for parameter_name, parameter_data in equipment.parameters.items():
        value = parameter_data["value"]
        if value is None:
            continue  # Skip updating if the value is None
        # device_name = (
        #     f"{equipment.group}_{equipment.equipment_type}_{equipment.equipment_id}"
        # )
        device_name = f"{equipment.group}_{equipment.equipment_type}"
        node_id = ua.NodeId(f"ns=2;s={parameter_name}_{device_name}")
        print("update.py, node_id", node_id)
        print("update.py, value", value)
        try:
            node = server.get_node(node_id)
            if node:
                node.set_value(value)
        except ua.UaStatusCodeError as e:
            print(f"Error updating node {node_id}: {e}")
