import sys
import math
import random
import copy
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.




class MapObj:
    """A class for every object on the game map"""
    x = 0;
    y = 0;
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def towards(self, object2, dis):
        obj1 = copy.deepcopy(self)
        obj2 = copy.deepcopy(object2)
        if distance(obj1, obj2) < dis:
            return obj2
        if obj1.x == obj2.x:
            x = obj1.x
            if obj1.y >= obj2.y:
                y =  obj1.y - dis
            else:
                y =  obj1.y + dis
            return MapObj(x, y)
        if obj2.x < obj1.x:
            dis = distance(obj1, obj2) - dis
            swap = obj1
            obj1 = obj2
            obj2 = swap
        m = (obj1.y - obj2.y)/(obj1.x - obj2.x)
        x_diff = math.sqrt((dis**2)/(1+m**2))
        y_diff = m*x_diff
        x = math.floor(obj1.x + x_diff)
        y = math.floor(obj1.y + y_diff)
        return MapObj(x, y)

    def towards(self, object2, dis):
        obj1 = copy.deepcopy(self)
        obj2 = copy.deepcopy(object2)
        if distance(obj1, obj2) < dis:
            return obj2
        if obj1.x == obj2.x:
            x = obj1.x
            if obj1.y >= obj2.y:
                y =  obj1.y - dis
            else:
                y =  obj1.y + dis
            return MapObj(x, y)
        if obj2.x < obj1.x:
            dis = distance(obj1, obj2) - dis
            swap = obj1
            obj1 = obj2
            obj2 = swap
        m = (obj1.y - obj2.y)/(obj1.x - obj2.x)
        x_diff = math.sqrt((dis**2)/(1+m**2))
        y_diff = m*x_diff
        x = math.floor(obj1.x + x_diff)
        y = math.floor(obj1.y + y_diff)
        return MapObj(x, y)


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
WANTED_INCOME = 4
KNIGHT_RADIUS = 20
QUEEN_RADIUS = 30
QUEEN_SPEED = 60
KNIGHT_SPEED = 100
MAP_LENGTH = 1920
MAP_HIGHT = 1000
TOWER_MAX_HP = 700
TOWER_MAX_RADIUS = 900

sold_out_mines = set([])
safe_point = MapObj(1,1)

def main():
    num_sites = int(input())
    sites_list = [] # a list of all the sites as Site objects
    train_next_turn = False
    for i in range(num_sites):
        site_id, x, y, radius = [int(j) for j in input().split()]
        sites_list.append(Site(site_id, x, y, radius))

    # game loop
    for turn in range(1000):
        print ('in for turn, turn:', turn, file=sys.stderr)
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
        print("safe_point:", safe_point, file=sys.stderr)
        if turn == 1:
            safe_point.set_coordinates(my_queen.x, my_queen.y)


        my_barracks_list = get_my_barracks(sites_list)
        seeing_sold_out_barracks = set([site for site in sites_list if site.remaining_gold == 0])
        sold_out_mines.update(seeing_sold_out_barracks)

        choose_action(sites_list, my_queen, enemy_queen, creep_list, my_barracks_list, touched_site)

        # if we have a barracks
        if len(my_barracks_list) > 0 and (gold > 80 or train_next_turn):
            print("TRAIN {0}".format(my_barracks_list[0].Id))
            train_next_turn = True
        else:
            print("TRAIN")

        if gold < 80 and train_next_turn != 0:
            print("dont train next turn", file = sys.stderr)
            train_next_turn = False

def choose_action(sites_list, my_queen, enemy_queen, creep_list, my_barracks_list, touched_site):
    my_goldmines = [site for site in sites_list if site.structure_type == GOLDMINE and site.owner == FRIENDLY]
    income = sum(map(lambda x: x.income_rate, my_goldmines)) # cal our total income from all the mines
    print ('income:', income, file=sys.stderr)
    touched_site = get_touched_site(sites_list, touched_site) # get the actual site by its Id
    enemy_creeps = [creep for creep in creep_list if creep.owner == ENEMY]
    sites_in_enemy_path = []
    if len([site for site in sites_list if site.structure_type == BARRACKS and site.owner == ENEMY]) > 0:
            sites_in_enemy_path = find_safe_point(sites_list)
            print("sites in path", *sites_in_enemy_path, file = sys.stderr)

    # if the queen toche a mine that isn't maxed
    if touched_site != None and touched_site.structure_type == GOLDMINE and touched_site.income_rate < touched_site.max_mine_rate:
        # upgrade the mine
        print ("BUILD {0} MINE".format(touched_site.Id))
    # if we don't get enough gold per turn and we the queen is safe
    elif income < WANTED_INCOME and is_safe(my_queen, enemy_creeps):
        # then build a mine on the closest posible site
        to_build_site = get_closest_possible_mine(my_queen, sites_list)
        print ("BUILD {0} MINE".format(to_build_site.Id) if to_build_site != None else "MOVE {0} {1}".format(safe_point.x, safe_point.y))
        # if we don'nt have any barracks
    elif len(my_barracks_list) == 0:
        # then build a knight barracks on the closest posible site
        closest_site = get_closest_site_without_strucure(my_queen, sites_list)
        print ("BUILD {0} BARRACKS-KNIGHT".format(closest_site.Id) if closest_site != None else "MOVE {0} {1}".format(safe_point.x, safe_point.y))
    else:
        # build a tower on the closest posible site / upgrade a touched tower if there is one
        to_build_site = get_closest_site_without_strucure(my_queen, sites_list)
        if touched_site != None and touched_site.owner == FRIENDLY and touched_site.structure_type == TOWER and touched_site.hp < TOWER_MAX_HP:
            to_build_site = touched_site
            print ("BUILD {0} TOWER".format(to_build_site.Id) if to_build_site != None else "MOVE {0} {1}".format(safe_point.x, safe_point.y))
        elif len(sites_in_enemy_path) > 0 and len([site for site in sites_list if site.structure_type == TOWER and site.owner == FRIENDLY]) > 3:
            to_brake = False
            for site in [site for site in sites_in_enemy_path if site.structure_type != GOLDMINE and site.structure_type != BARRACKS][:4]:
                if (site.structure_type != TOWER) or (site.structure_type == TOWER and site.hp < TOWER_MAX_HP*2//3):
                    print ("BUILD {0} TOWER".format(site.Id))
                    to_brake = True
                    break
            if not to_brake:
                print ("MOVE {0} {1}".format(safe_point.x, safe_point.y))
        else:
            print ("BUILD {0} TOWER".format(to_build_site.Id) if to_build_site != None else "MOVE {0} {1}".format(safe_point.x, safe_point.y))

def distance(obj1, obj2):
    return math.floor(math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2))

def get_my_barracks(sites_list):
    my_barracks_list = [site for site in sites_list if site.structure_type == BARRACKS and site.owner == FRIENDLY]
    return my_barracks_list

def get_sorted_site_list_without_strucure(my_queen, sites_list):
    sites_without_structer_list = [site for site in sites_list if site.owner != FRIENDLY and site.structure_type != TOWER]
    sites_without_structer_list = eliminate_dangerous_sites(sites_list, my_queen, sites_without_structer_list)
    sites_without_structer_list.sort(key=lambda site:(distance(my_queen, site))) # * distance(site, get_closest_point_on_edge(site)
    return sites_without_structer_list

def get_sorted_list_with_towers(my_queen, sites_list):
    sites_without_structer_list = [site for site in sites_list if not (bool(site.owner != FRIENDLY) ^ bool(site.structure_type != TOWER))]
    print("sites_without_structer_list:", *sites_without_structer_list, file=sys.stderr)
    sites_without_structer_list = eliminate_dangerous_sites(sites_list, my_queen, sites_without_structer_list)
    sites_without_structer_list.sort(key=lambda site:(distance(my_queen, site))) # * distance(site, get_closest_point_on_edge(site)
    return sites_without_structer_list

def get_closest_site_without_strucure(my_queen, sites_list):
    list = get_sorted_site_list_without_strucure(my_queen, sites_list)
    if len(list) == 0:
        return None
    return list[0]

def get_closest_point_on_edge(obj1):
    if safe_point.x < MAP_LENGTH/2:
        return MapObj(0, obj1.y)
    else:
        return MapObj(MAP_LENGTH, obj1.y)

def get_closest_possible_mine(my_queen, sites_list):
    possible_mines_list = [site for site in get_sorted_list_with_towers(my_queen, sites_list) if site.remaining_gold != 0 and site not in sold_out_mines]
    print("possible_mines_list:", *possible_mines_list, file=sys.stderr)
    if len(possible_mines_list) == 0:
        return None
    return possible_mines_list[0]

def eliminate_dangerous_sites(sites_list, my_queen, possible_sites):
    for tower in [site for site in sites_list if site.structure_type == TOWER and site.owner == ENEMY]:
        possible_sites = [site for site in possible_sites if distance(site, tower) > tower.attack_range]
    for site in possible_sites:
        next_site = False
        prev_step = my_queen
        for i in range(int(distance(my_queen, site)/QUEEN_SPEED)):
            step = prev_step.towards(site, QUEEN_SPEED)
            for tower in [site for site in sites_list if site.structure_type == TOWER and site.owner == ENEMY]:
                if distance(step, tower) < tower.attack_range:
                    possible_sites.remove(site)
                    next_site = True
                    break
            if next_site:
                break
            prev_step = step

    return possible_sites

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

def find_safe_point(sites_list, enemy_queen):
    enemy_barracks = [site for site in sites_list if site.structure_type == BARRACKS and site.owner == ENEMY]
    if len(enemy_barracks) == 0:
        enemy_barracks.append(enemy_queen)

    average_x = sum(enemy_barracks, key = lambda site: site.x) // len(enemy_barracks)
    average_y = sum(enemy_barracks, key = lambda site: site.y) // len(enemy_barracks)
    avarage_enemy_baracks = MapObj(average_x, average_y)
    pass
    return


def find_safe_point(sites_list):
    global safe_point
    enemy_barracks = [site for site in sites_list if site.structure_type == BARRACKS and site.owner == ENEMY]
    enemy_barracks.sort(key = lambda barrack: barrack.x)
    towers_in_path = []
    sites_in_path = []
    safe_points = [MapObj(0, 0), MapObj(0, MAP_HIGHT)]
    if safe_point.x>MAP_LENGTH/2:
        safe_points = [MapObj(MAP_LENGTH, MAP_HIGHT), MapObj(MAP_LENGTH, 0)]
    for point in safe_points:
        temp_towers_in_path = []
        temp_sites_in_path = []
        pos = enemy_barracks[0]
        while pos.x != point.x and pos.y != point.y:
            for site in sites_list:
                if site not in temp_sites_in_path and distance(site, pos) < TOWER_MAX_RADIUS / 2 - 300:
                    temp_sites_in_path.append(site)
                if site.owner == FRIENDLY and site.structure_type == TOWER and site not in towers_in_path and distance(site, pos) < site.attack_range/2:
                    temp_towers_in_path.append(site)
            pos = pos.towards(point, KNIGHT_SPEED * 2)
        if point == safe_points[0]:
            sites_in_path = temp_sites_in_path
            towers_in_path = temp_towers_in_path
        else:
            if len(temp_towers_in_path) > len(towers_in_path):
                safe_point = point
                sites_in_path = temp_sites_in_path
                for tower in temp_towers_in_path:
                    if tower not in sites_in_path:
                        sites_in_path.append(tower)
            else:
                safe_point = safe_points[0]
                for tower in towers_in_path:
                    if tower not in sites_in_path:
                        sites_in_path.append(tower)

    sites_in_path.sort(key = lambda site: distance(site, safe_point))
    print("temp_towers_in_path:", *temp_towers_in_path, file = sys.stderr)
    print("towers_in_path:", *towers_in_path, file = sys.stderr)
    return sites_in_path


main()
