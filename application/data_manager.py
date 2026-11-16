import json
from pathlib import Path
def load_from_json(my_file):
    try:
        with open (my_file,"r") as file:
            content = json.load(file)
            return content
    except:
        print ("unable to load json file")
    
def update_json(content,which_file):
    rooms_file = Path(__file__).parent.parent / "data"/"rooms.json"
    orders_file = Path(__file__).parent.parent / "data"/"orders.json"
    
    if which_file =="rooms":
        try:
            with open (rooms_file,"w",encoding="utf-8") as file:
                json.dump(content,file,indent=4)
                print ("rooms file updated")
        except json.JSONDecodeError as error:
            print("unable to update room file",error)
    else:
        try:
            with open (orders_file,"w",encoding="utf-8") as file:
                json.dump(content,file,indent=4)
                print ("orders file updated")
        except:
            print("unable to update orders file")