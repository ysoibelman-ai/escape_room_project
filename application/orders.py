from application.helper_functions import get_num,get_str,get_new_room_id,check_id_exists,get_new_id
from application.menus import order_menu
from application.data_manager import load_from_json,update_json
from datetime import datetime,date,time,timedelta
from application.rooms import is_active,get_room,right_amount_of_people


def order_manager(rooms:list,orders:list):
    while True:
        order_menu()
        menu_selection = get_num()
        match menu_selection:
            case 1:
                create_order(orders,rooms)
            case 2:
                show_orders(orders)
            case 3:
                search_order(orders)
            case 4:
                customers_orders(orders)
            case 5:
                show_orders_by_date(orders)
            case 6:
                update_order(orders,rooms)
            case 7:
                delete_order(orders)
            case 8:
                return
            case _:
                print ("Invalid Menu Selection")


def update_order(orders:list,rooms):
    order_id = get_str("Enter order id: ")
    if not get_order(order_id,orders):
        print("Order Does Not Exist")
        return False
    order = get_order(order_id,orders)
    order_room = get_room(rooms,order["room_id"])
    if order_room["is_active"] == False:
        print ("Room is not Active")
        return False
    
    order_details = ["booking_date","start_time","players"]
    changing = True
    
    while changing:
        change = get_str("Enter what you would like to change: ")
        
        if change not in order_details:
            print ("No such field")
            continue

        elif change == "booking_date":
            while True:
                my_date_time = get_date_time(order["start_time"])
                if not check_too_late(my_date_time,order_room,orders):
                    print ("not enough time")
                    continue
                if not check_clash(my_date_time,order_room,orders,order["booking_id"]):
                    print ("Clash with other Orders!!!!")
                    continue
                break
                
            value = str(my_date_time.date())
                
        elif change == "start_time":
            while True:
                my_date_time = get_date_time(order["booking_date"])
                if not check_too_late(my_date_time,order_room,orders):
                    print ("not enough time")
                    continue
                if not check_clash(my_date_time,order_room,orders,order["booking_id"]):
                    print ("Clash with other Orders!!!!")
                    continue
                break

            my_date_time = get_date_time()
            value = str(my_date_time.time())
        
        elif change == "players":
            while True:
                value = get_num("Enter Player Count: ")
                if not right_amount_of_people(order_room,value):
                    print ("room cannot hold that aount of peole")
                    continue

        order[change] = value
        continue_changing = get_num("Enter 1 to stop changing, any other number to continue changing")
        
        if continue_changing == 1:
            update_json(orders,"orders")
            changing = False     

def delete_order(orders):
    order_id = get_str("Enter order ID")
    if check_id_exists(order_id,"booking_id",orders):
        order = get_order(order_id,orders)
        if order["status"] == "Cancelled":
            print ("Order Already Cancelled")
            return
        order["status"] == "Cancelled"
        order["cancellation_fee"] = order["total_price"]*calculate_cancellation_fee(order)
        update_json(orders,"orders")
    else:
        print ("No order with that ID")

def show_orders_by_date(orders):
    date = get_str("Enter Date")
    orders_by_date = filter(lambda order: order["booking_date"] ==date, orders)
    if orders_by_date:
        show_orders(orders_by_date)
    else:
        print ("No orders in that date")

def customers_orders(orders):
    customer_name = get_str("Enter customers name: ")
    customers_orders = filter(lambda order: order["customer_name"] ==customer_name,orders)
    if customers_orders:
        show_orders(customers_orders)
    else:
        print ("there are no orders from this customer")


def search_order(orders):
    order_id = get_str("Enter Order ID")
    if not check_id_exists(order_id,"booking_id",orders):
        print ("No such order ID")
        return
    order = get_order(order_id,orders)
    print (order)

def get_order(order_id:str,orders:list):
    for order in orders:
        if order["booking_id"] == order_id:
            return order
    return False

def show_orders(orders):
    try:
        for order in orders:
            print (order)
    except:
        print ("no orders")

def create_order(orders:list,rooms:list):
    order = get_new_order_info(orders,rooms)
    orders.append(order)
    update_json(orders,"orders")

def get_new_order_info(orders,rooms):
    booking_id = get_new_id("booking_id",orders)
    customer_name = get_str("Enter Customer Name: ")
    
    while True:
        # Get Room ID
        room_id = get_str("Enter Room ID: ")
        if not check_id_exists(room_id,"room_id",rooms):
            print ("No room with that id")
            continue
        
        # Check If Room Is Active
        room =get_room(rooms,room_id)
        if not is_active(room):
            print ("room is not active, cannot book room")
            continue  
        break

    while True:
        # Right Amount Of People
        players = get_num("Enter Player Count: ")
        if not right_amount_of_people(room,players):
            print (f"people must be between {room["min_players"]} and {room["max_players"]}")
            continue
        break

    while True:
    # Get Booking Date and Hour
        my_date_time = get_date_time()
    # Date didnt Pass
        if not check_valid_date(my_date_time):
            print ("date already passed")
            continue
    # Hour Not Before 10
        if my_date_time.hour < 10:
            print ("too early in the day")
            continue

        if not check_too_late(my_date_time,room):
            print ("Too late in the day, not enough time to play room")
            continue

        if not check_clash(my_date_time,room,orders,booking_id):
            print ("Clash with other Orders!!!!")
            continue
        break

    booking_date = str(my_date_time.date())
    start_time = str(my_date_time.time())

    weekday = my_date_time.weekday()        
    total_price = room["price_per_player"] * players
    
    if weekday == 4 or weekday ==5:
        total_price = calculate_discount(total_price,players,True)
    else:
        total_price = calculate_discount(total_price,players)
    
    status = "Active"
    cancellation_fee = 0.0
    
    booking = {
            "booking_id": booking_id,
            "customer_name": customer_name,
            "room_id": room_id,
            "booking_date": booking_date,
            "start_time": start_time,
            "players": players,
            "total_price":total_price,
            "status": status,
            "cancellation_fee":cancellation_fee
            }
    return booking

def get_date_time(time_info="") -> datetime:
    while True:
        if time_info:
            if len (time_info) == 10:
                try:
                    year,month,day = time_info.split("-")
                    hour,minute = get_str("Enter Time: HH/MM").split("/")
                except ValueError:
                    print ("incorrect format")
                    continue

            elif len(time_info) < 10:
                try:
                    year,month,day = get_str ("Enter Date: YYYY/MM/DD").split("/")
                    hour,minute,seconds = time_info.split(":")
                except ValueError:
                    print ("incorrect format")
                    continue
        else:
            order_date = get_str ("Enter Date: YYYY/MM/DD/HH/MM")
        try:
            year,month,day,hour,minute = order_date.split("/")
        except ValueError:
            print ("incorrect format")
            continue
        try:
            order_date = datetime(year =int(year),month=int(month),day = int(day),hour = int(hour),minute = int(minute))
        except ValueError as error:
            print ("Invalid input, all values must be numbers ", error)
            continue
        return order_date


                    
def check_too_late(my_date_time:datetime,room):
    if my_date_time.hour > 22:
        return False
    
    if(my_date_time + timedelta(minutes=room["duration"])).hour > 22:
        return False
    
    return True

    
def check_clash(my_date_time:datetime,room,orders,my_order_id): 
    have_enough_time = True
    for order in orders:
        if order["booking_id"] == my_order_id:
            continue
        if order["room_id"] == room["room_id"]:
            if order["booking_date"] == str(my_date_time.date()):
                # print ("SAME DATE DUDE")

                # Second DT Object
                new_order_datetime = turn_into_date_time(order["booking_date"],order["start_time"])

                # Starts Too Early
                if my_date_time > new_order_datetime and my_date_time < new_order_datetime + timedelta(minutes=room["duration"] +15):
                    have_enough_time = False
                
                # Doesnt start early enough
                if new_order_datetime > my_date_time and my_date_time +timedelta(minutes=room["duration"] +15) > new_order_datetime:
                    have_enough_time = False
                
    return have_enough_time


def check_valid_date(order_date:datetime):
    if order_date < datetime.now():
        return False
    return True

def check_too_early(my_time):
   if my_time < time(hour = 10):
    return False
   return True

def turn_into_date_time(my_date:str,my_time:str):
    year,month,day,hour,minute,seconds = my_date.split("-") + my_time.split(":")
    return datetime(year =int(year),month=int(month),day = int(day),hour = int(hour),minute = int(minute),second=int(seconds))

def calculate_discount(total_price,players,weekend = False):
    if 5<=players<=6:
        total_price= total_price*0.9
    if players >= 7:
        total_price = total_price*0.85
    if weekend:
        total_price = total_price + total_price*0.15
    return round(total_price,2)

def calculate_cancellation_fee(order):
    order_date = turn_into_date_time(order["booking_date"],order["start_time"])
    if order_date - timedelta(hours=24) > datetime.now():
        return 1
    elif order_date - timedelta(hours=6) > datetime.now():
        return 0.25
    else:
        return 0.5
