from elevator import *
from random import randint

la_pampa = Building("La Pampa", 12)
la_pampa_01 = Elevator("Ascensor 01", la_pampa, 6)

names_file = open("nombres.csv", "r")
names = names_file.read().split(",")
names_file.close()

passenger_list = []
for i in range(1):
    passenger_list.append([randint(1, 12), names[randint(0, len(names))], 0])
    passenger_list.append([0, names[randint(0, len(names))], randint(1, 12)])

la_pampa.add_passengers(passenger_list)
