class Room:
    def __init__(self, x=None, y=None, w=None, h=None): 
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
        self.center = [(self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2]
    
    def intersects(self, room):
        if self.x1 > room.x2 or self.x2 < room.x1 or self.y1 > room.y2 or self.y2 < room.y1:
            return False
        return True

class Map:
    def __init__(self, map_w, map_h):
        self.map_w = map_w
        self.map_h = map_h
        self.map = [[0] * self.map_w for _ in range(self.map_h)]

    def draw_room(self, rooms):
        for room in rooms:
            x1, x2 = room.x1, room.x2
            y1, y2 = room.y1, room.y2
            cx, cy = room.center

            for i in range(x1, x2):
                for j in range(y1, y2):
                    if cx == i and cy == j:
                        self.map[i][j] = 2
                    else:
                        self.map[i][j] = 1
    
    def connect_crosswalk(self, rooms):
        for i in range(len(rooms) - 1):
            curr_room = rooms[i]
            next_room = rooms[i + 1]

            cx, cy = curr_room.center
            px, py = next_room.center

            cx_range = range(min(cx, px), max(cx, px) + 2)
            cy_range = range(min(cy, py), max(cy, py) + 2)

            for x in cx_range:
                self.map[x][cy + 1] = 1
                self.map[x][cy] = 1

            for y in cy_range:
                self.map[px + 1][y] = 1
                self.map[px][y] = 1

    def view_map(self):
        for i in self.map:
            for j in i:
                if j == 1:
                    print("\033[95m□\033[0m", end=" ")
                elif j == 2:
                    print("\033[103m□\033[0m", end=" ")
                else:
                    print("■", end=" ")
            print("")

import random

class Utils:
    def __init__(self, max_w, max_h, max_room_count):
        self.max_w = max_w
        self.max_h = max_h
        self.max_room_count = max_room_count

    def random_place_room(self, map):
        rooms = []
        count = 0

        while len(rooms) < self.max_room_count:
            w = random.randint(10, self.max_w - 1)
            h = random.randint(10, self.max_h - 1)
            x = random.randint(3, map.map_w - w - 3)
            y = random.randint(3, map.map_h - h - 3)

            new_room = Room(x, y, w, h)

            check_intersects = False

            for room in rooms:
                if new_room.intersects(room):
                    check_intersects = True
                    break

            if not check_intersects:
                count = 0
                rooms.append(new_room)

            count += 1

            if count == 1000:
                break
        return rooms 

def do_run():
    map = Map(256, 256)
    utils = Utils(50, 50, 1000)
    rooms = utils.random_place_room(map)
    map.connect_crosswalk(rooms)
    map.draw_room(rooms)
    map.view_map()

# start this program
do_run()

# reference URL : https://gamedevelopment.tutsplus.com/ko/-------gamedev-10099t

