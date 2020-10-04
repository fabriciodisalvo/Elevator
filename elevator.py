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
        self.elevator_history = []  # For graphical testing purposes only, not necessary to run elevator
        self.elevator_history_time = []  # For graphical testing purposes only, not necessary to run elevator
        self.time_running = 0  # For testing efficiency only, not necessary to run elevator
        self.people_served = 0  # For testing efficiency only, not necessary to run elevator

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
        self.time_running = self.time_running + 1  # Deceleration;  For testing efficiency only, not necessary to run elevator
        self.time_running = self.time_running + 3  # For testing efficiency only, not necessary to run elevator
        self.generate_graphical_data(3)  # For graphical testing purposes only, not necessary to run elevator
        passengers_to_unboard = [x for x in self.passenger_dict[self.current_floor]]
        for i in passengers_to_unboard:
            self.occupancy = self.occupancy - 1
            self.passenger_dict[self.current_floor].remove(i)
            self.time_running = self.time_running + 2  # For testing efficiency only, not necessary to run elevator
            self.generate_graphical_data(2)  # For graphical testing purposes only, not necessary to run elevator
            self.people_served = self.people_served + 1  # For testing efficiency only, not necessary to run elevator
            print("   %s has unboarded the elevator %s, which has now %s people aboard." % (i, self.elevator_id, self.occupancy))
        passengers_to_board = [x for x in self.building.waiting_dict[self.current_floor]]
        for i in passengers_to_board:
            if self.load_passenger(i[0], i[1]):
                self.building.waiting_dict[self.current_floor].remove(i)
                self.time_running = self.time_running + 2  # For testing efficiency only, not necessary to run elevator
                self.generate_graphical_data(2)  # For graphical testing purposes only, not necessary to run elevator
        print()

    def go_up(self):
        self.current_floor = self.current_floor + 1
        print("The Elevator %s is going up, now in floor %s." % (self.elevator_id, str(self.current_floor)))
        self.time_running = self.time_running + 1  # For testing efficiency only, not necessary to run elevator
        self.generate_graphical_data(1)  # For graphical testing purposes only, not necessary to run elevator
        if len(self.building.waiting_dict[self.current_floor]) > 0 or len(self.passenger_dict[self.current_floor]) > 0:
            print("   Opening door...")
            self.open_door()

    def go_down(self):
        self.current_floor = self.current_floor - 1
        print("The Elevator %s is going down, now in floor %s." % (self.elevator_id, str(self.current_floor)))
        self.time_running = self.time_running + 1  # For testing efficiency only, not necessary to run elevator
        self.generate_graphical_data(1)  # For graphical testing purposes only, not necessary to run elevator
        if len(self.building.waiting_dict[self.current_floor]) > 0 or len(self.passenger_dict[self.current_floor]) > 0:
            print("   Opening door...")
            self.open_door()

    def run_elevator(self):
        self.generate_graphical_data(1)  # For graphical testing purposes only, not necessary to run elevator
        if self.current_floor == 0 and (len(self.building.waiting_dict[0]) > 0 or len(self.passenger_dict[0]) > 0):
            print("The Elevator %s is on floor %s." % (self.elevator_id, str(self.current_floor)))
            print("   Opening door...")
            self.open_door()
        while self.current_floor < self.top_floor:
            next_waiting_floor = self.top_floor
            next_passenger_target_floor = self.top_floor
            for i in range(self.current_floor + 1, self.top_floor + 1):
                if len(self.building.waiting_dict[i]) > 0:
                    next_waiting_floor = i
                    break
            for i in range(self.current_floor + 1, int(self.top_floor) + 1):
                if len(self.passenger_dict[i]) > 0:
                    next_passenger_target_floor = i
                    break
            next_target_floor = min(next_passenger_target_floor, next_waiting_floor)
            for _ in range(next_target_floor - self.current_floor):
                self.go_up()
        while self.current_floor > 0:
            next_waiting_floor = 0
            next_passenger_target_floor = 0
            for i in range(self.current_floor - 1, 0 + 1, -1):
                if len(self.building.waiting_dict[i]) > 0:
                    next_waiting_floor = i
                    break
            for i in range(self.current_floor - 1, 0 + 1, -1):
                if len(self.passenger_dict[i]) > 0:
                    next_passenger_target_floor = i
                    break
            next_target_floor = max(next_passenger_target_floor, next_waiting_floor)
            for _ in range(self.current_floor - next_target_floor):
                self.go_down()
        return self.time_running, self.people_served, self.elevator_history, self.elevator_history_time

    def print_passenger_list(self):
        passenger_aboard_list = ""
        for i in self.passenger_dict.keys():
            if len(self.passenger_dict[i]) == 1:
                passenger_aboard_list = passenger_aboard_list + ("There is %s person aboard going to floor %s.\n" % (len(self.passenger_dict[i]), str(i)))
            elif len(self.passenger_dict[i]) > 1:
                passenger_aboard_list = passenger_aboard_list + ("There are %s people aboard going to floor %s.\n" % (len(self.passenger_dict[i]), str(i)))
        if len(passenger_aboard_list) > 1:
            print("%s. People on board:" % self.elevator_id)
            print(passenger_aboard_list)
    
    def generate_graphical_data(self, time_spent):  # For graphical testing purposes only, not necessary to run elevator
        state = []
        for i in range(self.building.number_of_floors):
            passengers_in_this_floor = 0
            if self.current_floor == i:
                passengers_in_this_floor = self.occupancy
            floor_state = (len(self.building.waiting_dict[i]), passengers_in_this_floor)
            state.append(floor_state)
        self.elevator_history.append(state)
        self.elevator_history_time.append(time_spent)
