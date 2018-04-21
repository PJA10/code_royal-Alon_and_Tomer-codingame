import sys
import math
import random
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

NO_STRUCTURE = -1
TOWER = 1
BARRACKS = 2
FRIENDlY = 0
ENEMY = 1
QUEEN = -1
KNIGHT = 0
ARCHER = 1
GIANT = 2
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
            # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
            site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
            right_site = next(filter(lambda site: site.Id == site_id, sites_list)) # the site with with site_id as his id
            right_site.set_site_data(ignore_1, ignore_2, structure_type, owner, param_1, param_2)

        print(sites_list, file= sys.stderr)

        my_queen = None;
        creep_list = []
        num_units = int(input())
        for i in range(num_units):
            # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
            x, y, owner, unit_type, health = [int(j) for j in input().split()]
            if unit_type == QUEEN and owner == FRIENDlY:
                my_queen = Unit(x, y, owner, unit_type, health)
            elif unit_type == QUEEN and owner == ENEMY:
                enemy_queen = Unit(x, y, owner, unit_type, health)
            else:
                creep_list.append(Unit(x, y, owner, unit_type, health))

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        my_barracks_list = get_my_barracks(sites_list)
        if len(my_barracks_list) == 0:
            



        d = float('inf')
        closet_no_structued_site = 0
        for site in sites_list:
            if site.owner != 0 and distance(site, my_queen) < d:
                closet_no_structued_site = site
                d = distance(site, my_queen)
        # First line: A valid queen action
        # Second line: A set of training instructions
        rand = random.randint(0,2)
        barracks_type = "KNIGHT"
        #if rand == 1:
        #   barracks_type = "ARCHER"
        print("BUILD", closet_no_structued_site.Id, "BARRACKS-" + barracks_type)
        closet_knight_barrack_to_enemy_queen = Site(0,0,0,0)
        if gold>80:
            d = float('inf')
            for site in sites_list:
                if site.structure_type == 2 and site.owner == 0 and distance(site, enemy_queen) < d:
                    closet_knight_barrack_to_enemy_queen = site
                    d = distance(site, enemy_queen)

        print("TRAIN", closet_knight_barrack_to_enemy_queen.Id)


def distance(obj1, obj2):
    return math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)

def get_my_barracks(sites_list):
    my_barracks_list = [for site in sites_list if site.structure_type == BARRACKS and site.owner == FRIENDlY]
    return my_barracks_list

class MapObj:
    """A class for every object on the game map"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Site(MapObj):
    def __init__(self, Id, x, y, radius):
        super().__init__(x, y)
        self.Id = Id
        self.radius = radius

    def set_site_data(self, ignore_1, ignore_2, structure_type, owner, param_1, param_2):
        self.ignore_1 = ignore_1
        self.ignore_2 = ignore_2
        self.owner = owner
        self.structure_type = structure_type
        if structure_type == TOWER:
            self.hp = param_1
            self.attack_range = param_2
        if structure_type == BARRACKS:
            self.num_of_turns_for_set = param_1
            self.creep_type = param_2


class Unit(MapObj):
    def __init__(self, x, y, owner, type, health):
        super().__init__(x, y)
        self.owner = owner
        self.unit_type = type
        self.health = health

main()
