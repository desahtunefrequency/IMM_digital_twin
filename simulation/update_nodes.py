from opcua import ua


def update_imm_nodes(server, equipment, device_name):
    injection_time_node = server.get_node(
        ua.NodeId(f"ns=2;s=InjectionTime_{device_name}")
    )
    if injection_time_node:
        injection_time_node.set_value(equipment.injection_time)

    cooling_time_node = server.get_node(ua.NodeId(f"ns=2;s=CoolingTime_{device_name}"))
    if cooling_time_node:
        cooling_time_node.set_value(equipment.cooling_time)

    demolding_time_node = server.get_node(
        ua.NodeId(f"ns=2;s=DemoldingTime_{device_name}")
    )
    if demolding_time_node:
        demolding_time_node.set_value(equipment.demolding_time)

    cycle_count_node = server.get_node(ua.NodeId(f"ns=2;s=CycleCount_{device_name}"))
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


def update_iml_nodes(server, equipment, device_name):
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


def update_chil_nodes(server, equipment, device_name):
    delivery_temp_stationary_node = server.get_node(
        ua.NodeId(f"ns=2;s=DeliveryTempStationary_{device_name}")
    )
    if delivery_temp_stationary_node:
        delivery_temp_stationary_node.set_value(equipment.delivery_temp_stationary)

    return_temp_stationary_node = server.get_node(
        ua.NodeId(f"ns=2;s=ReturnTempStationary_{device_name}")
    )
    if return_temp_stationary_node:
        return_temp_stationary_node.set_value(equipment.return_temp_stationary)

    # ... (Similarly update other CHIL nodes: pressure_stationary, delivery_temp_moving, etc.)


def update_c_disp_nodes(server, equipment, device_name):
    cycle_time_node = server.get_node(ua.NodeId(f"ns=2;s=CycleTime_{device_name}"))
    if cycle_time_node:
        cycle_time_node.set_value(equipment.cycle_time)


def update_m_con_nodes(server, equipment, device_name):
    working_time_node = server.get_node(ua.NodeId(f"ns=2;s=WorkingTime_{device_name}"))
    if working_time_node:
        working_time_node.set_value(equipment.working_time)


def update_robo_nodes(server, equipment, device_name):
    cycle_time_node = server.get_node(ua.NodeId(f"ns=2;s=CycleTime_{device_name}"))
    if cycle_time_node:
        cycle_time_node.set_value(equipment.cycle_time)
