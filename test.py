from icecream import ic

field = [[' ' for x in range(8)] for i in range(8)]
ships = {x:0 for x in range(1, 5)}

def check_diagonale(field, x, y): #I love Yan. 
    coords_changes = ((1, 1), (-1, -1), (1, -1), (-1, 1))

    for t in coords_changes:
        x1, y1 = t
        x1 += x
        y1 += y
        ic(x1, y1)
        if x1 == 8 or x1 == -1 or y1 == -1 or y1 == 8:
            continue

        if field[y1][x1] == 'x':
            return False

    return True

def ships_nearly(field, x, y):
    ships_near = []
    for x1 in range(-1, 2):
        for y1 in range(-1, 2):
            if 8 > y + y1 >= 0 and 8 > x + x1 >= 0:
                if field[y + y1][x + x1] == 'x':
                    ships_near.append((x+x1, y+y1))
    
    if (x, y) in ships_near:
        ships_near.remove((x, y))

    return ships_near

def get_ship_len(field, x, y):
    lenght = 1
    
    x1, y1 = x, y
    ships_near = ships_nearly(field, x, y)

    if len(ships_near) == 0:
        return 1

    if abs(ships_near[0][0] - x):
        while x1 > 0 and field[y][x1-1] == 'x':
            lenght += 1
            x1 -= 1
        x1 = x
        while x1 < 7 and field[y][x1 + 1] == 'x':
            lenght += 1
            x1 += 1
    else:
        while y1 > 0 and field[y1 - 1][x] == 'x':
            lenght += 1
            y1 -= 1
        y1 = y
        while y1 < 7 and field[y1 + 1][x] == 'x':
            lenght += 1
            y1 += 1
    
    return lenght

def check_ship_len(lenght, ships):
    ic(ships)
    #if lenght == 1 and ships[1] == 5:
        #return False

    ic(lenght, ships)
    if lenght == 1 and ships[1] == 5 or lenght == 2 and ships[2] == 3 or lenght == 3 and ships[3] == 2 or lenght == 4 and ships[4] == 1 or lenght == 5:
    #if lenght == 6 or lenght == 2 and ships[2] == 3 or lenght == 2 and ships[3] == 2 or lenght == 5 and ships[4] == 1:
        return False
    return True

def write_ship_data(ships, field, x, y):
    lenght = get_ship_len(field, x, y)
    if lenght != 1:
        #ic(ships_nearly(field, x, y))
        if len(ships_nearly(field, x, y)) == 2:
            for ship in ships_nearly(field, x, y):
                #It's works but what price had I payed?
                field[y][x] = ' '
                ships[get_ship_len(field, *ship)] -= 1
                field[y][x] = 'x'
        else:
            ships[lenght-1] -= 1
    
    ships[lenght] += 1


while True and False:  
    x, y = [int(x) for x in input('Введите координаты: ').split()]
    ic(check_diagonale(field, x, y))
    if field[y][x] == 'x':
        ships[get_ship_len(field, x, y)] -= 1
        field[y][x] = ' '
        for ship in ships_nearly(field, x, y):
            ships[get_ship_len(field, *ship)] += 1
        ic(field)
        continue

    if check_diagonale(field, x, y):
        #ic(check_ship_len(get_ship_len(field, x, y), ships))
        if check_ship_len(get_ship_len(field, x, y), ships):
            field[y][x] = "x"
            write_ship_data(ships, field)
            ic(ships)
    ic(field)

