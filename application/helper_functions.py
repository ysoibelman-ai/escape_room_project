from application.validations import valid_num,valid_str
def get_str(msg=""):
    while True:
        string = input(msg)
        if valid_str(string):
            return string
        else:
            print ("string musy not be empty")
        
def get_num (msg =""):
    while True:
        num = input(msg)
        if valid_num(num):
            return int(num)

def get_difficutly(msg=""):
    difficulties = ["Hard","Medium","Easy"]
    while True:
        difficulty = input(msg).strip().capitalize()
        if difficulty in difficulties:
            return difficulty
        else:
            print ("Invalid difficulty")

def get_max_player(min_players,msg="",):
    while True:
        num = input(msg)
        if valid_num(num) and int(num) > min_players:
            return int(num)
        print ("max players must be larger num than min players")



def get_new_room_id(rooms:list,msg=""):
    while True:
        new_id = get_str(msg)
        if any(room["room_id"] == new_id for room in rooms):
            print ("id already taken")
        else:
            return new_id


def get_new_id(id_type,my_list):
    while True:
        new_id = get_str(f"Enter new {id_type}")
        if any(item[id_type] == new_id for item in my_list):
            print ("ID already taken")
        else:
            return new_id


def check_id_exists(new_id,id_type,my_list):
    for item in my_list:
        if item[id_type] == new_id:
            return True
    return False

