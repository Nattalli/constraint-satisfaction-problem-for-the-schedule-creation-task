import itertools
from typing import List, Tuple, Dict, Optional


class Subject:
    def __init__(self, name: str) -> None:
        self.name = name


class Teacher:
    def __init__(self, name: str) -> None:
        self.name = name


class Group:
    def __init__(self, name: str, num_students: int) -> None:
        self.name = name
        self.num_students = num_students


class Room:
    def __init__(self, name: str, capacity: int) -> None:
        self.name = name
        self.capacity = capacity


def convert_for_printing(items):
    if type(items) == list:
        return ", ".join(item.name for item in items)
    return items.name


teachers = [
    Teacher(name)
    for name in (
        "0 Shevchenko",
        "1 Kovalenko",
        "2 Melnyk",
        "3 Tkachuk",
        "4 Hrytsenko",
        "5 Bondarenko",
        "6 Ponomarenko",
        "7 Petrenko",
        "8 Lysenko",
        "9 Marchenko",
        "10 Dmytrenko",
        "11 Zaytsev",
        "12 Ivanchenko",
        "13 Savchenko",
        "14 Vasylenko",
    )
]

subjects = [
    Subject(name)
    for name in (
        "0 Introduction to Computer Science",
        "1 Data Structures and Algorithms",
        "2 Operating Systems",
        "3 Computer Networks",
        "4 Database Systems",
        "5 Software Engineering",
        "6 Artificial Intelligence",
        "7 Machine Learning",
        "8 Computer Graphics",
        "9 Web Development",
        "10 Cybersecurity",
        "11 Human-Computer Interaction",
        "12 Compiler Design",
        "13 Parallel and Distributed Computing",
        "14 Computer Architecture",
    )
]

groups = [
    Group("MI", 15),
    Group("TTP-41", 25),
    Group("TTP-42", 24),
    Group("TK-1", 30),
    Group("TK-2", 20),
]

rooms = (
    [Room(f"Room_{i}", 50) for i in range(4)]
    + [Room(f"Room_{i + 4}", 20) for i in range(10)]
    + [Room(f"Room_{i + 14}", 15) for i in range(6)]
)

weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}
times = {1: "8:40-10:15", 2: "10:35-12:10", 3: "12:20-13:55"}


def constraints(c1, c2):
    if c1 is None or c2 is None:
        return True
    if c1[1] == c2[1] and c1[4] == c2[4]:
        return False
    if c1[2].num_students > c1[3].capacity or c2[2].num_students > c2[3].capacity:
        return False
    if set(c1[2].name).intersection(set(c2[2].name)) and c1[4] == c2[4]:
        return False
    if c1[3] == c2[3] and c1[4] == c2[4]:
        return False
    return True


def forward_checking(assignments, variables, domain):
    for j, variable in enumerate(variables):
        if variable not in assignments:
            if assignments and assignments[-1] is not None and len(assignments) > 0:
                if not constraints(assignments[-1], domain[variable][0]):
                    domain[variable] = [c for c in domain[variable] if constraints(assignments[-1], c)]
            else:
                domain[variable] = [c for c in domain[variable] if constraints(None, c)]


def mrv(assignments, variables, domain):
    remaining_domains = [len(domain[var]) for var in variables if var not in assignments]
    if remaining_domains:
        return min(remaining_domains)
    return None


def backtracking(assignments: Dict[int, Tuple], variables: List[int], domain: Dict[int, List[Tuple]]) -> Optional[Dict[int, Tuple]]:
    if len(assignments) == len(variables):
        return assignments
    unassigned = [var for var in variables if var not in assignments]
    forward_checking(assignments, variables, domain)

    min_remaining_value = mrv(assignments, variables, domain)
    if min_remaining_value is None:
        return None

    for variable in unassigned:
        if len(domain[variable]) == min_remaining_value:
            for value in domain[variable]:
                assignments[variable] = value
                result = backtracking(assignments, variables, domain)
                if result is not None:
                    return result
                del assignments[variable]

    return None


def create_schedule():
    all_combinations = list(itertools.product(subjects, teachers, groups, rooms, weekdays.keys(), times.keys()))
    domain = {i: [c] for i, c in enumerate(all_combinations)}
    variables = list(range(len(all_combinations)))
    schedule = backtracking({}, variables, domain)
    return schedule


def print_schedule(schedule):
    print(f"{'День':<10} {'Час':<15} {'Предмет':<40} {'Викладач':<30} {'Група':<15} {'Лекція'}")
    print("-" * 115)

    sorted_schedule = sorted(schedule, key=lambda cls: (cls[4], cls[5]))
    for cls in sorted_schedule:
        subject, teacher, group, room, weekday, time_slot = cls
        print(
            f"{weekdays[weekday]:<10} {times[time_slot]:<15} {subject.name:<40} "
            f"{teacher.name:<30} {group.name:<15} {room.name}"
        )


if __name__ == "__main__":
    schedule = create_schedule()
    if schedule is not None:
        print_schedule(schedule)
    else:
        print("No valid schedule found.")
