"""
This helperclass is just to simulate the response of a fake API and to get back fake data.
"""

# Importing libraries
from faker import Faker
from random import uniform
from time import sleep
import json



class GET():
    def __init__(self):
        self.return_timer = uniform(2,5)
        fake = Faker(["en_US"])
        return_data = fake.profile()
        self.return_dict = {"first_name":return_data["name"].split()[0],
                    "last_name":return_data["name"].split()[1],
                    "gender":return_data["sex"],
                    "blood_group":return_data["blood_group"]}
    
    def get_data(self):
        return json(self.return_dict)
    
