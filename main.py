from application.menus import main_menu
from application.helper_functions import get_num
from application.rooms import room_manager
from application.orders import order_manager
from application.reports import report_manager
from application.data_manager import load_from_json,update_json
import os
from pathlib import Path

def main():
    rooms_file = Path(__file__).parent / "data"/"rooms.json"
    orders_file = Path(__file__).parent / "data"/"orders.json"
    while True:
        rooms = load_from_json(rooms_file)
        orders = load_from_json(orders_file)
        main_menu()
        main_menu_selection = get_num()
        match main_menu_selection:
            case 1:
                room_manager(rooms,orders)
                os.system("clear")
            case 2:
                order_manager(rooms,orders)
                os.system("clear")
            case 3:
                report_manager()
                os.system("clear")
            case 4:
                exit()
            case _:
                print ("Invalid Menu Selection")


if __name__ == "__main__":
    main()