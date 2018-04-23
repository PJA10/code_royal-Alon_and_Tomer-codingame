import sys
import math
import random
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
WANTED_INCOME = 8
KNIGHT_RADIUS = 20
QUEEN_RADIUS = 30
KNIGHT_SPEED = 100
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
            site_id, remaining_gold, max_mine_rate, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
            right_site = next(filter(lambda site: site.Id == site_id, sites_list)) # the site with with site_id as his id
            right_site.set_site_data(remaining_gold, max_mine_rate, structure_type, owner, param_1, param_2)

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
        
        my_barracks_list = get_my_barracks(sites_list)
        
        choose_action(sites_list, my_queen, creep_list, my_barracks_list, touched_site)
        
        # if we have a barracks
        if len(my_barracks_list) > 0:
            print("TRAIN {0}".format(my_barracks_list[0].Id))
        else:
            print("TRAIN")
            
def choose_action(sites_list, my_queen, creep_list, my_barracks_list, touched_site):
    my_goldmines = get_my_goldmines(sites_list)
    income = sum(map(lambda x: x.income_rate, my_goldmines)) # cal our total income from all the mines
    print ('income:', income, file=sys.stderr)
    touched_site = get_touched_site(sites_list, touched_site) # get the actual site by its Id
    enemy_creeps = [creep for creep in creep_list if creep.owner == ENEMY] 
    
    # if the queen toche a mine that isn't maxed
    if touched_site != None and touched_site.structure_type == GOLDMINE and touched_site.income_rate < touched_site.max_mine_rate:
        # upgrade the mine
        print ("BUILD {0} MINE".format(touched_site.Id))
    # if we don'nt have any barracks
    elif len(my_barracks_list) == 0:
        # then build a knight barracks on the closest posible site
        closest_site = get_closest_site_wothout_strucure(my_queen, sites_list)
        print ("BUILD {0} BARRACKS-KNIGHT".format(closest_site.Id) if closest_site != None else "MOVE 0 0")
    # if we don't get enough gold per turn and we the queen is safe 
    elif income < WANTED_INCOME and is_safe(my_queen, enemy_creeps):
        # then build a mine on the closest posible site
        to_build_site = get_closest_possible_mine(my_queen, sites_list)
        print ("BUILD {0} MINE".format(to_build_site.Id) if to_build_site != None else "MOVE 0 0")
    else:
        # build a tower on the closest posible site / upgrade a touched tower if there is one
        to_build_site = get_closest_site_wothout_strucure(my_queen, sites_list)
        if touched_site != None and touched_site.owner == FRIENDLY and touched_site.structure_type == TOWER and touched_site.hp < 700:
            to_build_site = touched_site
        print ("BUILD {0} TOWER".format(to_build_site.Id) if to_build_site != None else "MOVE 0 0")
            

def distance(obj1, obj2):
    return math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)

def get_my_barracks(sites_list):
    my_barracks_list = [site for site in sites_list if site.structure_type == BARRACKS and site.owner == FRIENDLY]
    return my_barracks_list

def get_my_goldmines(sites_list):
    gold_mines = [site for site in sites_list if site.structure_type == GOLDMINE and site.owner == FRIENDLY]
    return gold_mines

def get_closest_site_wothout_strucure(my_queen, sites_list):
    sites_wothout_structer_list = [site for site in sites_list if site.owner != FRIENDLY and site.structure_type != TOWER]
    for tower in [site for site in sites_list if site.structure_type == TOWER and site.owner == ENEMY]:
        sites_wothout_structer_list = [site for site in sites_wothout_structer_list if distance(site, tower) > tower.attack_range]
    sites_wothout_structer_list.sort(key=lambda site:distance(my_queen, site))
    if len(sites_wothout_structer_list) == 0:
        return None
    return sites_wothout_structer_list[0]

def get_closest_possible_mine(my_queen, sites_list):
    possible_mines_list = [site for site in sites_list if site.owner != FRIENDLY and site.structure_type != TOWER and site.remaining_gold != 0]
    for tower in [site for site in sites_list if site.structure_type == TOWER and site.owner == ENEMY]:
        possible_mines_list = [site for site in possible_mines_list if distance(site, tower) > tower.attack_range]
    possible_mines_list.sort(key=lambda site:distance(my_queen, site))
    print("possible_mines_list:", *possible_mines_list, file=sys.stderr)
    if len(possible_mines_list) == 0:
        return None
    return possible_mines_list[0]

def get_touched_site(sites_list, touched_site):
    touched_site = [site for site in sites_list if site.Id == touched_site]
    if len(touched_site) != 0:
        touched_site = touched_site[0]
        return touched_site
    return None

def is_safe(my_queen, enemy_creeps):
    is_safe = True
    if len(enemy_creeps) != 0:
        closest_creep = min(enemy_creeps, key=lambda creep: distance(my_queen, creep))
        if distance(closest_creep, my_queen) < KNIGHT_RADIUS + QUEEN_RADIUS + KNIGHT_SPEED*2:
            is_safe = False
    return is_safe

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


    def set_site_data(self, remaining_gold, max_mine_rate, structure_type, owner, param_1, param_2):
        self.owner = owner
        self.structure_type = structure_type
        self.max_mine_rate = max_mine_rate
        self.remaining_gold = remaining_gold
        if structure_type == TOWER:
            self.hp = param_1
            self.attack_range = param_2
        if structure_type == BARRACKS:
            self.num_of_turns_for_set = param_1
            self.creep_type = param_2
        if structure_type == GOLDMINE:
            self.income_rate = param_1

    def __str__(self):
        return "(id = {0} ({1}, {2}))".format(self.Id, self.x, self.y)

class Unit(MapObj):
    def __init__(self, x, y, owner, type, health):
        super().__init__(x, y)
        self.owner = owner
        self.unit_type = type
        self.health = health

    def __str__(self):
        return "(id = {0} ({1}, {2}))".format(self.type, self.x, self.y)
main()
