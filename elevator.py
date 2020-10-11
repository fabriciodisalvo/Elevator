class Building:
    def __init__(self, name, number_of_floors):
        self.name = name
        self.number_of_floors = number_of_floors
        self.elevators = []
        self.waiting_dict = {}
        for i in range(int(number_of_floors) + 1):
            self.waiting_dict[i] = []

    def add_person(self, floor, person_waiting_name, person_target_floor):
        self.waiting_dict[floor].append((person_waiting_name, person_target_floor))
        self.activate_switchboard(floor)

    def activate_switchboard(self, floor):
        for elevator in self.elevators:
            if elevator.current_floor < floor:
                elevator.cue.append(floor)
                elevator.run_elevator()
                break
        self.elevators[0].cue.append(floor)
        self.elevators[0].run_elevator()

    def print_waiting_list(self):
        print("Building %s. %i floors." % (self.name, self.number_of_floors))
        first_passenger = False
        for i in self.waiting_dict.keys():
            waiting_cue = len(self.waiting_dict[i])
            if not first_passenger and waiting_cue > 0:
                first_passenger = True
                print("Waiting Cue:")
            if waiting_cue == 1:
                print("At floor %s, there is %s person waiting." % (str(i), waiting_cue))
            elif waiting_cue > 1:
                print("At floor %s, there are %s people waiting." % (str(i), waiting_cue))
        print()


class Elevator:
    def __init__(self, elevator_id, building, capacity=20):
        self.elevator_id = elevator_id
        self.capacity = capacity
        self.occupancy = 0
        self.current_floor = 0
        self.passenger_dict = {}
        self.building = building
        self.building.elevators.append(self)
        self.top_floor = self.building.number_of_floors
        for i in range(int(self.top_floor) + 1):
            self.passenger_dict[i] = []
        self.cue = []

    def load_passenger(self, person_waiting_name, person_target_floor):
        if self.occupancy == self.capacity:
            print("Elevator is Full")
            return 0
        else:
            self.occupancy = self.occupancy + 1
            self.passenger_dict[person_target_floor].append(person_waiting_name)
            print("   %s has boarded the elevator %s, which has %s people aboard." % (person_waiting_name, self.elevator_id, self.occupancy))
            return 1

    def open_door(self):
        passengers_to_unboard = [x for x in self.passenger_dict[self.current_floor]]
        for i in passengers_to_unboard:
            self.occupancy = self.occupancy - 1
            self.passenger_dict[self.current_floor].remove(i)
            print("   %s has unboarded the elevator %s, which has now %s people aboard." % (i, self.elevator_id, self.occupancy))
        passengers_to_board = [x for x in self.building.waiting_dict[self.current_floor]]
        for i in passengers_to_board:
            if self.load_passenger(i[0], i[1]):
                self.cue.append(i[1])
                self.building.waiting_dict[self.current_floor].remove(i)
        print()

    def go_up(self):
        self.current_floor = self.current_floor + 1
        print("The Elevator %s is going up, now in floor %s." % (self.elevator_id, str(self.current_floor)))
        if len(self.building.waiting_dict[self.current_floor]) > 0 or len(self.passenger_dict[self.current_floor]) > 0:
            print("   Opening door...")
            self.open_door()

    def go_down(self):
        self.current_floor = self.current_floor - 1
        print("The Elevator %s is going down, now in floor %s." % (self.elevator_id, str(self.current_floor)))
        if len(self.building.waiting_dict[self.current_floor]) > 0 or len(self.passenger_dict[self.current_floor]) > 0:
            print("   Opening door...")
            self.open_door()

    def run_elevator(self):
        if len(self.cue) == 0:
            return
        else:
            next_target_floor = min(self.cue)
            if next_target_floor == self.current_floor:
                print("The Elevator %s is on floor %s." % (self.elevator_id, str(self.current_floor)))
                print("   Opening door...")
                self.open_door()
            elif next_target_floor > self.current_floor:
                for _ in range(next_target_floor - self.current_floor):
                    self.go_up()
            else:
                for _ in range(self.current_floor - next_target_floor):
                    self.go_down()
            self.cue.remove(next_target_floor)
            print(self.cue, ' faltan, asi que running again...')
            self.run_elevator()
