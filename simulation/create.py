import sqlite3
from machines.imm import IMM
from machines.iml import IML
from machines.chil import CHIL
from machines.m_con import M_CON
from machines.c_disp import C_DISP
from machines.robo import ROBO


def create_equipment(equipment_type, device_name):

    device_name_parts = device_name.split("_")

    equipment_id = device_name_parts[
        -1
    ]  # Fetching the last element which should be equipment_id
    print(equipment_id)
    if equipment_type == "IMM":
        return IMM(int(equipment_id))
    else:
        return None
