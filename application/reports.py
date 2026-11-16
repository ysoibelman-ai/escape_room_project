from application.menus import report_menu
from application.helper_functions import get_str, get_num,check_id_exists
from application.rooms import get_room
def report_manager(orders:list,rooms:list):
    while True:
        report_menu()
        menu_selection = get_num()
        match menu_selection:
            case 1:
                show_orders(orders)
            case 2:
                show_orders(orders,False)
            case 3:
                total_active_orders_income(orders)
            case 4:
                total_cancellation_fee(orders)
            case 5:
                print(most_popular_room(orders))
            case 6:
                print(orders_per_room(orders,rooms))
            case 7:
                print (percentage_room_usage(orders,rooms))
            case 8:
                return
            case _:
                print ("invalid menu selection")

def show_orders(orders:list,is_active = True):
    if is_active:
        print([filter(lambda order: order["is_active"] == "Active",orders)])
    else:
        print([filter(lambda order: order["is_active"] == "Cancelled",orders)])

def total_active_orders_income(orders:list):
    print(f"Total Income From All Active Orders Is {sum(order["total_price"] for order in orders if order["is_active"] == "Active")}")


def total_cancellation_fee(orders:list):
    print (f"Total Cancellation fee is: {sum(order["cancellation_fee"] for order in orders if order["is_active"] == "Cancelled" )}")


def orders_per_room(orders:list):
    orders_per_room_dict = {}
    for order in orders:
        if order["room_id"] not in orders_per_room:
            orders_per_room_dict["room_id"] = 1
        else:
            orders_per_room_dict["room_id"]+=1
    return orders_per_room_dict

def most_popular_room(orders:list):
    orders_per_room_dict = orders_per_room(orders)
    max_orders = 0
    for key,value in orders_per_room_dict.item():
        if value > max_orders:
            max_orders = value
            max_room = key

    return max_room

def percentage_room_usage(orders:list,rooms:list):
    while True:
        room_id = get_str("Enter Room ID: ")
        if not check_id_exists(room_id,"room_id",rooms):
            print ("No room with that id")
            continue
        break
    room =get_room(rooms,room_id)
    year = input("Enter year: ")
    month = input("Enter month: ")
    day = input("Enter day: ")
    my_date = f"{year}-{month}-{day}"
    total_time = 0

    for order in orders:
        if order["booking_date"] == my_date:
            if order["room_id"] == room_id:
                total_time += room["duration"] + 15
    
    total_time = total_time*100 / (12*60)
    total_time = f"{total_time}% daily use"
    return total_time
        





