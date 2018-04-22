import sys
import math
import random
from functools import reduce
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

NO_STRUCTURE = -1
TOWER = 1
BARRACKS = 2
FRIENDLY = 0
ENEMY = 1
QUEEN = -1
KNIGHT = 0
ARCHER = 1
GIANT = 2
GOLDMINE = 0
def main():
    num_sites = int(input())
    sites_list = [] # a list of all the sites as Site objects

    for i in range(num_sites):
        site_id, x, y, radius = [int(j) for j in input().split()]
        sites_list.append(Site(site_id, x, y, radius))

    # game loop
    while True:
        # touched_site: -1 if none
        gold, touched_site = [int(i) for i in input().split()]
        for i in range(num_sites):
            # ignore_1: used in future leagues
            # ignore_2: used in future leagues
            # structure_type: -1 = No structure, 2 = Barracks
            # owner: -1 = No structure, 0 = FRIENDLY, 1 = Enemy
            site_id, remaining_gold, max_mine_size, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
            right_site = next(filter(lambda site: site.Id == site_id, sites_list)) # the site with with site_id as his id
            right_site.set_site_data(remaining_gold, max_mine_size, structure_type, owner, param_1, param_2)

        print(*sites_list, file= sys.stderr)

        my_queen = None;
        creep_list = []
        num_units = int(input())
        for i in range(num_units):
            # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
            x, y, owner, unit_type, health = [int(j) for j in input().split()]
            if unit_type == QUEEN and owner == FRIENDLY:
                my_queen = Unit(x, y, owner, unit_type, health)
            elif unit_type == QUEEN and owner == ENEMY:
                enemy_queen = Unit(x, y, owner, unit_type, health)
            else:
                creep_list.append(Unit(x, y, owner, unit_type, health))

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)
        my_goldmines = get_my_goldmines(sites_list)
        income = sum(map(lambda x: x.income_rate, my_goldmines))
        print ('income:', income, file=sys.stderr)

        my_barracks_list = get_my_barracks(sites_list)
        if len(my_barracks_list) == 0:
            closest_site = get_closest_site_wothout_strucure(my_queen, sites_list)
            print ("BUILD {0} MINE".format(closest_site.Id))
            # print ("BUILD {0} BARRACKS-KNIGHT".format(closest_site.Id))
            print("TRAIN")
        else:
            to_build_site = get_closest_site_wothout_strucure(my_queen, sites_list)
            touched_site = [site for site in sites_list if site.Id == touched_site]
            if len(touched_site) != 0:
                touched_site = touched_site[0]
                if touched_site.structure_type == TOWER and touched_site.hp < 700:
                    to_build_site = touched_site
            print ("BUILD {0} TOWER".format(to_build_site.Id))
            print("TRAIN", my_barracks_list[0].Id)


def distance(obj1, obj2):
    return math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)

def get_my_barracks(sites_list):
    my_barracks_list = [site for site in sites_list if site.structure_type == BARRACKS and site.owner == FRIENDLY]
    return my_barracks_list

def get_my_goldmines(sites_list):
    gold_mines = [site for site in sites_list if site.structure_type == GOLDMINE and site.owner == FRIENDLY]
    return gold_mines

def get_closest_site_wothout_strucure(my_queen, sites_list):
    sites_wothout_structer_list = [site for site in sites_list if site.owner != FRIENDLY]
    sites_wothout_structer_list.sort(key=lambda site:distance(my_queen, site))
    return sites_wothout_structer_list[0]

class MapObj:
    """A class for every object on the game map"""
    x = 0;
    y = 0;
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Site(MapObj):
    def __init__(self, Id, x, y, radius):
        super().__init__(x, y)
        self.Id = Id
        self.radius = radius


    def set_site_data(self, remaining_gold, max_mine_size, structure_type, owner, param_1, param_2):
        self.owner = owner
        self.structure_type = structure_type
        if structure_type == TOWER:
            self.hp = param_1
            self.attack_range = param_2
        if structure_type == BARRACKS:
            self.num_of_turns_for_set = param_1
            self.creep_type = param_2
        if structure_type == GOLDMINE:
            self.income_rate = param_1
            self.max_mine_size = max_mine_size
            self.remaining_gold = remaining_gold

    def __str__(self):
        return "(id = {0} ({1}, {2}))".format(self.Id, self.x, self.y)

class Unit(MapObj):
    def __init__(self, x, y, owner, type, health):
        super().__init__(x, y)
        self.owner = owner
        self.unit_type = type
        self.health = health

main()
