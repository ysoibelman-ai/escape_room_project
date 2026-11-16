from application.menus import rooms_menu
from application.helper_functions import get_num,get_str,get_difficutly,get_max_player,check_id_exists,get_new_id
from application.data_manager import update_json

def room_manager(rooms:list,orders:list):
    while True:
        rooms_menu()
        menu_selection = get_num()
        match menu_selection:
            case 1:
                show_rooms(rooms)
            case 2:
                show_room_info(rooms)
            case 3:
                add_room(rooms)
            case 4:
                update_room_details(rooms)
            case 5:
                room_activation(rooms)
            case 6:
                return
            case _:
                print ("Invalid Menu Selection")

def room_activation(rooms):
    room_id = get_str("Enter room id: ")
    if not get_room(rooms,room_id):
            print("Room Does Not Exist")
            return
    else:
        room = get_room(rooms,room_id)
        room["is_active"] = not room["is_active"]
        print (room)
        update_json(rooms,"rooms")
        print (f"Room status changes from {not room['is_active']} to {room['is_active']}")

def add_room(rooms):
    new_room = get_new_room_info()
    rooms.append(new_room)
    update_json(rooms,"rooms")

def update_room_details(rooms):
    room_id = get_str("Enter room id: ")
    if not get_room(rooms,room_id):
            print("Room Does Not Exist")
            return
    
    room = get_room(rooms,room_id)
    room_details = ["room_id","name","difficulty","duration","min_players","max_players","price_per_player","is_active"]
    changing = True
    while changing:
        change = get_str("Enter what you would like to change: ")
        if change not in room_details:
            print ("No such field")
            continue

        if change in ["duration","min_players","price_per_player"]:
            value = get_num(f"Enter new {change}: ")
        elif change == "name":
            value = get_str(f"Enter new {change}: ")
        elif change == "room_id":
            while True:
                value = get_new_id("room_id",rooms)
                if not check_id_exists(value,"room_id",rooms):
                    print ("id taken")
                    continue
                break
        elif change == "difficulty":
            value = get_difficutly(f"Enter {change}: ")
        elif change == "max_players":
            value = get_max_player(f"Enter {change}: ",room["min_players"])

        room[change] = value
        continue_changing = get_num("Enter 1 to stop changing, any other number to continue changing")
        if continue_changing == 1:
            update_json(rooms,"rooms")
            changing = False

def get_new_room_info():
    room_id = ("Enter room id: ")
    name = get_str("Enter room name: ")
    difficulty = get_difficutly("Enter difficulty: ")
    duration = get_num("Enter duration: ")
    min_players = get_num("Enter min players: ")
    max_players = get_max_player(min_players,"Enter max players: ")
    price_per_player = get_num("Enter price per player: ")
    is_active = True

    room = { "room_id": room_id,
            "name": name,
            "difficulty": difficulty,
            "duration": duration,
            "min_players": min_players,
            "max_players": max_players,
            "price_per_player": price_per_player,
            "is_active": is_active}
    
    return room

def show_rooms(rooms:list):
    try:
        for room in rooms:
            print (room["name"])
    except:
        print ("no rooms")

def show_room_info(rooms:list):
    room_id = get_str("Enter Room ID: ")
    if not get_room(rooms,room_id):
        print("Room Does Not Exist")
        return
    else:
        print (get_room(rooms,room_id))
    
def get_room(rooms:list,room_id:int):
    for room in rooms:
        if room["room_id"] == room_id:
            return room
    return False

def is_active(room):
    return room["is_active"]

def right_amount_of_people(room,people):
    return people <= room["max_players"] and people >= room["min_players"]