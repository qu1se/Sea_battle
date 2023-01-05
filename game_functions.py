
#получение даты 
async def get_data(state):
    data = await state.storage.get_data(state.bot, 'general_data')
    return data['games'][str((await state.get_data())['room'])]

#проверка диагоналей, ограничение полем 
def check_diagonale(field, x, y):
    coords_changes = ((1, 1), (-1, -1), (1, -1), (-1, 1))

    for t in coords_changes:
        x1, y1 = t
        x1 += x
        y1 += y
        #ic(x1, y1)
        if x1 == 8 or x1 == -1 or y1 == -1 or y1 == 8:
            continue

        if field[y1][x1] == '🚢':
            return False

    return True

#проверка кораблей рядом, ограничение полем
def ships_nearly(field, x, y, ship_type='🚢'):

    ships_near = []
    for x1 in range(-1, 2):
        for y1 in range(-1, 2):
            if 8 > y + y1 >= 0 and 8 > x + x1 >= 0:
                if field[y + y1][x + x1] in ship_type:
                    ships_near.append((x+x1, y+y1))
    
    if (x, y) in ships_near:
        ships_near.remove((x, y))

    return ships_near


def get_ship_len(field, x, y, ship_type='🚢', return_coords:bool = False):

    lenght = 1

    coords = [[x, y]]

    x1, y1 = x, y
    ships_near = ships_nearly(field, x, y, ship_type)

    
    if len(ships_near) == 0:
        if return_coords:
            return lenght, coords
        return lenght

    if abs(ships_near[0][0] - x):
        while x1 > 0 and field[y][x1-1] in ship_type:
            lenght += 1
            x1 -= 1
            coords.append([x1, y])
        x1 = x
        while x1 < 7 and field[y][x1 + 1] in ship_type:
            lenght += 1
            x1 += 1
            coords.append([x1, y])
    else:
        while y1 > 0 and field[y1 - 1][x] in ship_type:
            lenght += 1
            y1 -= 1
            coords.append([x, y1])
        y1 = y
        while y1 < 7 and field[y1 + 1][x] in ship_type:
            lenght += 1
            y1 += 1
            coords.append([x, y1])
    
    if return_coords:
        return lenght, coords
    return lenght

def check_ship_len(lenght, ships):
    #if lenght == 1 and ships[1] == 5:
        #return False

    if lenght == 1 and ships[1] == 4 or lenght == 2 and ships[2] == 3 or lenght == 3 and ships[3] == 2 or lenght == 4 and ships[4] == 1 or lenght == 5:
    
        return False
    return True

#запись данных
def write_ship_data(ships, field, x, y):
    lenght = get_ship_len(field, x, y)
    if lenght != 1:
        #ic(ships_nearly(field, x, y))
        if len(ships_nearly(field, x, y)) == 2:
            for ship in ships_nearly(field, x, y):
                field[y][x] = ' '
                ships[get_ship_len(field, *ship)] -= 1
                field[y][x] = '🚢'
        else:
            ships[lenght-1] -= 1
    
    ships[lenght] += 1

def ships_count(field):
    return sum([x.count('🚢') for x in field])

def is_cracked(field, x, y):
    normal_lenght = get_ship_len(field, x, y, 'x🚢')

    crack_lenght = get_ship_len(field, x, y, 'x')

    if crack_lenght != normal_lenght:
        return False
    return True
    
def put_dorts(field, x, y):
    ships_coords = get_ship_len(field, x, y, 'x', True)[1]

    print(ships_coords)
    for coords in ships_coords:
        for empty_place in ships_nearly(field, *coords, ship_type=' '):
            x, y = empty_place
            field[y][x] = '.'

def remove_ship(field, ships, x, y):
    ships[get_ship_len(field, x, y)] -= 1
    field[y][x] = ' '
    for ship in ships_nearly(field, x, y):
        ships[get_ship_len(field, *ship)] += 1

def main_check(field, ships, x, y):
    if check_diagonale(field, x, y) and check_ship_len(get_ship_len(field, x, y), ships):
        write_ship_data(ships, field, x, y)
        return True
    return False

