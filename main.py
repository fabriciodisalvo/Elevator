from elevator import *

la_pampa = Building("La Pampa", 12)
la_pampa_01 = Elevator("Ascensor 01", la_pampa, 6)

names_file = open("nombres.csv", "r")
names = names_file.read().split(",")
names_file.close()

la_pampa.add_person(0, names[0], 12)
la_pampa.add_person(11, names[1], 0)
la_pampa.print_waiting_list()
la_pampa_01.run_elevator()
