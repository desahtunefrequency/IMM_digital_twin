import streamlit as st
from opcua import Client
import sqlite3

# OPC UA Server URL
url = "opc.tcp://localhost:4840"

# Connect to the SQLite database
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Get list of systems and equipment types from the database
cursor.execute("SELECT system_name FROM system")
systems = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT DISTINCT equipment_type FROM equipment")
equipment_types = [row[0] for row in cursor.fetchall()]
conn.close()

# Connect to the OPC UA server
client = Client(url)
try:
    client.connect()

    # Streamlit App Title
    st.title("Injection Molding Simulation UI")

    # Sidebar for system and equipment type selection
    selected_system = st.sidebar.selectbox("Select System", options=systems)
    selected_type = st.sidebar.selectbox(
        "Select Equipment Type", options=equipment_types
    )

    # Get the root node and retrieve all nodes
    root_node = client.get_root_node()

    def browse_nodes(node):
        node_list = []
        for child in node.get_children():
            node_list.append(child)
            node_list.extend(browse_nodes(child))  # Recursively browse children
        return node_list

    all_nodes = browse_nodes(root_node)

    # Filter equipment nodes based on selected system and equipment type
    filtered_nodes = []
    for node in all_nodes:
        node_id_str = node.nodeid.to_string()
        browse_name = node.get_browse_name().Name
        parts = browse_name.split("_")  # Split the BrowseName
        if (
            node_id_str.startswith("s=ns=2;")
            and parts[0] == selected_system  # Check system
            and len(parts) >= 3  # Ensure enough parts for type
            and parts[1] == selected_type  # Check equipment type
        ):
            filtered_nodes.append(node)

    # Display data for the filtered equipment
    if filtered_nodes:
        for node in filtered_nodes:
            st.subheader(f"Equipment: {node.get_browse_name().Name}")
            for variable in node.get_variables():
                variable_name = variable.get_browse_name().Name
                variable_value = variable.get_value()
                st.write(f"{variable_name}: {variable_value}")
    else:
        st.info(
            f"No equipment found for system: {selected_system} and type: {selected_type}"
        )

except Exception as e:
    st.error(f"Error connecting to OPC UA server: {e}")

finally:
    client.disconnect()
