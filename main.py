from elevator import *
from random import randint

my_building = Building("My Office Building", 12)
my_building_01 = Elevator("01", my_building, 6)

names_file = open("nombres.csv", "r")
names = names_file.read().split(",")
names_file.close()

passenger_list = []
for i in range(10):
    passenger_list.append([0, names[randint(0, len(names)-1)], randint(1, 12)])
    passenger_list.append([randint(1, 12), names[randint(0, len(names)-1)], 0])
my_building.add_passengers(passenger_list)
