from opcua import Server, ua


def add_opc_ua_nodes(server, equipment_node, equipment_type, device_name):

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
