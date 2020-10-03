from elevator import *

la_pampa = Building("La Pampa", 12)
la_pampa_01 = Elevator("Ascensor 01", la_pampa, 6)

la_pampa.add_person(0, "Fabri", 12)
la_pampa.add_person(0, "Rusa", 12)
la_pampa_01.run_elevator()
