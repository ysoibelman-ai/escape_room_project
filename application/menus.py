def main_menu():
    print ("""
=================
    MAIN MENU
=================
Choose Option:

1. Room Management
2. Order Management
3. Reports
4. Exit
    """)


def rooms_menu():
        print ("""
=================
    ROOM MENU
=================
Chosse Option:

1. Show Rooms
2. Show Room Info
3. Add Room
4. Update Room Details
5. Activate / Deactivate Room
6. Return To Main Menu        
        """)


"""
המערכת תאפשר:
יצירת הזמנה חדשה.
הצגת כל ההזמנות.
חיפוש הזמנה לפי מזהה.
הצגת ההזמנות של לקוח מסוים.
הצגת ההזמנות לפי תאריך.
שינוי פרטי הזמנה קיימת.
ביטול הזמנה.


"""
def order_menu():
      print ("""
===================
    ORDER MENU
===================
Choose Option:

1. Create New Order
2. Show All Orders
3. Search Order By ID
4. Show Customers Orders
5. Show Orders by Date
6. Update Order
7. Delete Order
8. Return To Main Menu
""")

def report_menu():
      print ("""
====================
    REPORTS MENU
====================
Choose Option:

1. All Active Orders
2. All Cancelled Orders
3. Total Income From Active Orders
4. Total Cancellation Fee
5. Most Popular Room
6. Number of Orders Per Room
7. % Use of Room In Given Date 
8. Return to Main menu
""")
      