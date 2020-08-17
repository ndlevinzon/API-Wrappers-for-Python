import requests
import json
import pandas as pd
from pyfiglet import Figlet

def students():
    custom_fig = Figlet(font='5lineoblique')
    print(custom_fig.renderText('Random Person Gen'))
    loop = input("Insert Number of People You Want to Print to students.json: ")

    count = 0
    while count < int(loop):
        r = requests.get('https://randomuser.me/api/?format=json&nat=US&inc=gender,name,location,email,dob').json()
        try:
            with open("people.json", "r+") as file:
                data = json.load(open("people.json", 'r'))
                data.append(r)
                json.dump(data, file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("people.json", 'w') as file:
                data = [r]
                json.dump(data, file, indent=4)
        count = count +1

    next = input("DONE! Press 'l' to list in console and commit to .csv, 'r' to restart, or 'q' to quit: ")
    if next == "l":
       df = pd.read_json("students.json")
       df.to_csv("students.csv")

    if next == "r":
        students()
    if next == "q":
        open("people.json", "w")
        open("people.csv", "w")
        exit()
students()

