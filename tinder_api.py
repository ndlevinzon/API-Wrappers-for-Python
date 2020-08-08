# Import modules/libraries
import requests
import os
import sys
from random import random
from datetime import datetime
from time import sleep
from geopy.geocoders import Nominatim
from secrets import apitoken

TINDER_URL = "https://api.gotinder.com"
geolocator = Nominatim(user_agent="Downloader")
PROF_FILE = r"..\profiles.txt"


class tinderAPI():

    def __init__(self, token):
        self._token = token

    def profile(self):
        data = requests.get(TINDER_URL + "/v2/profile?include=account%2Cuser",
                            headers={"X-Auth-Token": self._token}).json()
        return list(data["data"], self)

    def matches(self, limit=10):
        data = requests.get(TINDER_URL + f"/v2/matches?count={limit}", headers={"X-Auth-Token": self._token}).json()
        return list(map(lambda match: Person(match["person"], self), data["data"]["matches"]))

    def like(self, user_id):
        data = requests.get(TINDER_URL + f"/like/{user_id}", headers={"X-Auth-Token": self._token}).json()
        return {
            "is_match": data["match"],
            "liked_remaining": data["likes_remaining"]
        }

    def dislike(self, user_id):
        requests.get(TINDER_URL + f"/pass/{user_id}", headers={"X-Auth-Token": self._token}).json()
        return True

    def nearby_persons(self):
        data = requests.get(TINDER_URL + "/v2/recs/core", headers={"X-Auth-Token": self._token}).json()
        return list(map(lambda user: Person(user["user"], self), data["data"]["results"]))


class Person(object):

    def __init__(self, data, api):
        self.api = api

        self.id = data["_id"]
        self.name = data.get("name", "Unknown")

        self.bio = data.get("bio", "")
        self.distance = data.get("distance_mi", 0) / 1.60934

        self.birth_date = datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]

        self.images = list(map(lambda photo: photo["url"], data.get("photos", [])))

        self.jobs = list(
            map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")},
                data.get("jobs", [])))
        self.schools = list(map(lambda school: school["name"], data.get("schools", [])))

        if data.get("pos", False):
            self.location = geolocator.reverse(f'{data["pos"]["lat"]}, {data["pos"]["lon"]}')

    def __repr__(self):
        return f"{self.id}  -  {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"

    def like(self):
        return self._api.like(self.id)

    def dislike(self):
        return self._api.dislike(self.id)

    # Download Functionality
    def download_images(self, folder=".", sleep_max_for=0):
        with open(PROF_FILE, "r") as f:
            lines = f.readlines()
            if self.id in lines:
                return
        with open(PROF_FILE, "a") as f:
            f.write(self.id + "\r\n")
        index = -1

        for image_url in self.images:
            index += 1
            req = requests.get(image_url, stream=True)
            if req.status_code == 200:
                with open(f"{folder}/{self.id}_{self.name}_{index}.jpeg", "wb") as f:
                    f.write(req.content)
            sleep(random() * sleep_max_for)


def Download_IMG():
    # Download Logic
    data_max = False
    n0 = 0
    n1 = 0

    for r, d, files in os.walk(r"A:\\CNN\images\unclassified"):
        n0 += len(files)
        print("files in ./images/unclassified = {}".format(n0))

    persons = api.nearby_persons()
    for Person in persons:
        if data_max == False:
            Person.download_images(folder=r"A:\\CNN\images\unclassified", sleep_max_for=random() * 3)

            for r, d, files in os.walk(r"A:\\CNN\images\unclassified"):
                n1 += len(files)
                if n0 != n1:
                    n0 = len(files)
                    print("files in ./images/unclassified = {}".format(n0))
                if n0 >= 2501:
                    data_max = True

            sleep(random() * 10)
            sleep(random() * 10)

        if data_max == True:
            sys.exit("Data Full! Transitioning to Classification...")


if __name__ == "__main__":
    # SYS Printout
    print("$pwd was ['" + os.getcwd() + "']")
    print("$argv was", sys.argv)
    print("$sys.executable was ['" + sys.executable + "']")

    # Image Source Logic
    token = apitoken
    api = tinderAPI(token)

    # Download 2500 Training Images
    while True:
        try:
            Download_IMG()

        # Restart when Image Queue is Empty in 1 Hour
        except KeyError or TypeError:
            print("Image Queue Empty! Restarting in 1 Hour...")
            sleep(3600)
            Download_IMG()
