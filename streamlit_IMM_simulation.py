import streamlit as st
import sqlite3
from opcua import Client

# Database connection
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# OPC UA client
client = Client("opc.tcp://localhost:4840")
client.connect()

# Function to fetch equipment data from database
def get_equipment_data(equipment_id):
    cursor.execute("SELECT * FROM main.Equipment WHERE SAP=?", (equipment_id,))
    return cursor.fetchone()

def get_unique_ids():
    cursor.execute("SELECT distinct SAP FROM main.Equipment")
    unique_ids = [row[0] for row in cursor.fetchall()]
    return unique_ids
# Function to add new equipment to database
def add_equipment(equipment_type, group):
    cursor.execute("INSERT INTO main.Equipment (type, group_delete) VALUES (?, ?)", (equipment_type, group))
    conn.commit()
    st.success("Equipment added successfully!")

# Sidebar for equipment selection and addition
st.sidebar.title("Equipment Control Panel")
equipment_id = st.sidebar.selectbox("Equipment ID", options=get_unique_ids())
equipment_data = get_equipment_data(equipment_id)

if equipment_data:
    equipment_type = equipment_data[4]
    group = equipment_data[1]
    
    device_name = f"{group}_{equipment_type}_{equipment_id}"
    
    st.sidebar.write(f"**Type:** {equipment_type}")
    st.sidebar.write(f"**Group:** {group}")

    # Display equipment properties based on type
    if equipment_type == "IMM":
        injection_time = client.get_node(f"ns=2;s=InjectionTime_{device_name}").get_value()
        cooling_time = client.get_node(f"ns=2;s=CoolingTime_{device_name}").get_value()
        # ... (Add other IMM properties)
    elif equipment_type == "IML":
        labeling_state = client.get_node(f"ns=2;s=LabelingState_{device_name}").get_value()
        # ... (Add other IML properties)
    # ... (Add other equipment types)

    # Display equipment properties in main area
    st.title(f"Equipment: {device_name}")
    st.write(f"**Type:** {equipment_type}")
    st.write(f"**Group:** {group}")
    # ... (Display properties based on equipment type)

else:
    st.sidebar.warning("Equipment not found!")

# Add new equipment form
with st.sidebar.expander("Add New Equipment"):
    equipment_type = st.selectbox("Type", ["IMM", "IML", "CHIL", "C_DISP", "M_CON", "ROBO"])
    group = st.text_input("Group")
    if st.button("Add Equipment"):
        add_equipment(equipment_type, group)

# Disconnect from OPC UA server and database
client.disconnect()
conn.close()