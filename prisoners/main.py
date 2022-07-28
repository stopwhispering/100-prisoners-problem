from random import choice, sample
from typing import Literal, Dict, List, Tuple


class Box:
    def __init__(self, number_box: int, number_prisoner: int):
        self.number_box = number_box
        self._number_prisoner = number_prisoner

    def get_prisoner_number(self) -> int:
        return self._number_prisoner


class Room:
    def __init__(self, n_prisoners: int, verbose: bool):
        self.n_prisoners = n_prisoners
        self.boxes: Dict[int, Box] = {}
        self.verbose = verbose
        prisoner_numbers = [i for i in range(1, n_prisoners + 1)]
        for i in range(1, n_prisoners + 1):
            prisoner_number = choice(prisoner_numbers)
            prisoner_numbers.remove(prisoner_number)
            self.boxes[i] = Box(number_box=i, number_prisoner=prisoner_number)

    def get_box_by_position(self, position: int) -> Box:
        return self.boxes[position]

    def find_closed_loops(self) -> List[List]:
        closed_loops: Dict[Tuple, List] = dict()

        for i in range(self.n_prisoners):
            number_prisoner_correct = i + 1
            box_numbers_not_checked = list(self.boxes.keys())
            current_loop = []
            box_number = number_prisoner_correct

            while True:
                # start new loop

                if (box_number not in box_numbers_not_checked) != (box_number in current_loop):
                    print('EROROOR''')

                if box_number not in box_numbers_not_checked:
                    box_number = choice(box_numbers_not_checked)

                # continue in current loop
                current_loop.append(box_number)
                box = self.get_box_by_position(box_number)
                box_numbers_not_checked.remove(box_number)
                if number_prisoner_correct == box.get_prisoner_number():
                    # generic version of the loop (sorted numbers) shared by all prisoners in that loop
                    closed_loop_tuple = tuple(sorted(current_loop))
                    if closed_loop_tuple in closed_loops:
                        if self.verbose:
                            print(f'Prisoner {number_prisoner_correct} uses an already found loop of '
                                  f'size {len(closed_loop_tuple)}')
                    else:
                        if self.verbose:
                            print(f'Prisoner {number_prisoner_correct} uses a new loop of '
                                  f'size {len(closed_loop_tuple)}')
                        closed_loops[tuple(sorted(current_loop))] = current_loop
                    break
                else:
                    box_number = box.get_prisoner_number()
        assert sum(len(c) for c in closed_loops) == self.n_prisoners
        return list(closed_loops.values())


class Prisoner:
    def __init__(self, number: int):
        self.number = number

    def find_box_randomly(self, room: Room, max_tries: int) -> bool:
        box_numbers_all = list(room.boxes.keys())
        box_numbers = sample(box_numbers_all, max_tries)
        for box_number in box_numbers:
            box = room.get_box_by_position(box_number)
            if box.get_prisoner_number() == self.number:
                return True

        return False

    def find_box_loop(self, room: Room, max_tries: int) -> bool:
        box_numbers_not_checked = list(room.boxes.keys())

        box_number = self.number

        left_tries = max_tries
        while left_tries:
            left_tries -= 1

            # start new loop
            if box_number not in box_numbers_not_checked:
                box_number = choice(box_numbers_not_checked)

            # continue in current loop
            box = room.get_box_by_position(box_number)
            box_numbers_not_checked.remove(box_number)
            if self.number == box.get_prisoner_number():
                return True
            else:
                box_number = box.get_prisoner_number()

        return False

    def find_box(self, room: Room, max_tries: int, strategy: Literal["random", "loop"]) -> bool:
        if strategy == "random":
            return self.find_box_randomly(room, max_tries=max_tries)
        elif strategy == "loop":
            return self.find_box_loop(room, max_tries=max_tries)


class Simulation:
    def __init__(self, n_prisoners: int, strategy: Literal["random", "loop"], verbose: bool):
        self.n_prisoners = n_prisoners
        self.strategy = strategy
        self.verbose = verbose
        self.success = None

        self.prisoners = [Prisoner(i) for i in range(1, self.n_prisoners + 1)]
        self.room = Room(self.n_prisoners, verbose=self.verbose)

    def find_closed_loops(self) -> List[List]:
        """only find the closed loops --> shortcut"""
        return self.room.find_closed_loops()

    def run(self, max_tries: int):
        """run the complete simulation"""
        for prisoner in self.prisoners:
            found = prisoner.find_box(self.room, max_tries=max_tries, strategy=self.strategy)
            if not found:
                if self.verbose:
                    print(f"Prisoner {prisoner.number} failed to find his box")
                self.success = False
                return

        if self.verbose:
            print("All prisoners found their box")
        self.success = True


def run_simulation(count_prisoners: int, max_tries: int, strategy: Literal["random", "loop"], verbose: bool) -> bool:
    """run a complete simulation and return the success of the simulation"""
    simulation = Simulation(count_prisoners, strategy, verbose)
    simulation.run(max_tries=max_tries)
    return simulation.success


def evaluate_closed_loops(n_prisoners: int,
                          strategy: Literal["random", "loop"]) -> Tuple[Dict[int, int], List[List]]:
    """setup a prisoners room, find cloesd loops and return them along  with prisoner mappings for gui display"""
    simulation = Simulation(n_prisoners=n_prisoners, strategy=strategy, verbose=False)
    box_numbers_with_prisoner_numbers = {box.number_box: box.get_prisoner_number() for box in
                                         simulation.room.boxes.values()}
    closed_loops = simulation.find_closed_loops()
    return box_numbers_with_prisoner_numbers, closed_loops


def main(n_prisoners: int, n_simulations: int, strategy: Literal["random", "loop"], verbose: bool):
    """run a number of full simulations and return the success rate"""
    results = []
    for _ in range(n_simulations):
        results.append(run_simulation(n_prisoners, max_tries=n_prisoners // 2, strategy=strategy, verbose=verbose))

    percentage_true = results.count(True) / len(results)
    print(f'In {percentage_true:.2%} ({results.count(True)}/{len(results)}) of the simulations '
          f'with strategy "{strategy}", all {n_prisoners} prisoners found their box.')
