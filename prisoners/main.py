from random import choice, sample
from typing import Literal, Dict


class Box:
    def __init__(self, number_box: int, number_prisoner: int):
        self.number_box = number_box
        self._number_prisoner = number_prisoner

    def get_prisoner_number(self) -> int:
        return self._number_prisoner


class Room:
    def __init__(self, count_prisoners: int):
        self.count_prisoners = count_prisoners
        self.boxes: Dict[int, Box] = {}
        prisoner_numbers = [i for i in range(1, count_prisoners + 1)]
        for i in range(1, count_prisoners + 1):
            prisoner_number = choice(prisoner_numbers)
            prisoner_numbers.remove(prisoner_number)
            self.boxes[i] = Box(number_box=i, number_prisoner=prisoner_number)

    def get_box_by_position(self, position: int) -> Box:
        return self.boxes[position]


class Prisoner:
    def __init__(self, number: int,  max_tries: int):
        self.number = number
        self.max_tries = max_tries

    def find_box_randomly(self, room: Room) -> bool:
        box_numbers_all = list(room.boxes.keys())
        box_numbers = sample(box_numbers_all, self.max_tries)
        for box_number in box_numbers:
            box = room.get_box_by_position(box_number)
            if box.get_prisoner_number() == self.number:
                return True

        return False

    def find_box_loop(self, room: Room) -> bool:
        box_numbers_not_checked = list(room.boxes.keys())

        box_number = self.number

        left_tries = self.max_tries
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

    def find_box(self, room: Room, strategy: Literal["random", "loop"]) -> bool:
        if strategy == "random":
            return self.find_box_randomly(room)
        elif strategy == "loop":
            return self.find_box_loop(room)


def run_simulation(count_prisoners: int, max_tries: int, strategy: Literal["random", "loop"], verbose: bool) -> bool:

    prisoners = [Prisoner(i, max_tries=max_tries) for i in range(1, count_prisoners+1)]
    room = Room(count_prisoners)

    for prisoner in prisoners:
        found = prisoner.find_box(room, strategy=strategy)
        if not found:
            if verbose:
                print(f"Prisoner {prisoner.number} failed to find his box")
            return False

    if verbose:
        print("All prisoners found their box")
    return True


def main(n_prisoners: int, n_simulations: int, strategy: Literal["random", "loop"], verbose: bool):

    results = []
    for _ in range(n_simulations):
        results.append(run_simulation(n_prisoners, max_tries=n_prisoners // 2, strategy=strategy, verbose=verbose))

    percentage_true = results.count(True) / len(results)
    print(f'In {percentage_true:.2%} ({results.count(True)}/{len(results)}) of the simulations '
          f'with strategy "{strategy}", all {n_prisoners} prisoners found their box.')

    a = 1
