from enum import Enum


class Raid(Enum):
    def __init__(self, full_name, player_size):
        self.full_name = full_name
        self.player_size = player_size

    kara = ("Karazhan", 10)
    ml = ("Magtheridon's Lair", 25)
    gl = ("Gruul's Lair", 25)
    tk = ("Tempest Keep", 25)
    ssc = ("Serpentshrine Cavern", 25)
    bt = ('Black Temple', 25)
    mh = ('Mount Hyjal', 25)
    za = ("Zul'Aman", 10)
    sp = ('Sunwell Plateau', 25)
