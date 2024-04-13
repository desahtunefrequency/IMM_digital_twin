import sqlite3
from machines.imm import IMM
from machines.iml import IML
from machines.chil import CHIL
from machines.m_con import M_CON
from machines.c_disp import C_DISP
from machines.robo import ROBO


def create_equipment(equipment_type, device_name):
    if equipment_type == "IMM":
        return IMM()
    elif equipment_type == "IML":
        return IML()
    elif equipment_type == "CHIL":
        return CHIL()
    elif equipment_type == "M_CON":
        return M_CON()
    elif equipment_type == "C_DISP":
        return C_DISP()
    elif equipment_type == "ROBO":
        return ROBO()
    else:
        return None
