import sys
from collections import deque
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import floor, ceil
from multiprocessing import Pool
from pathlib import Path
from typing import NamedTuple, Iterable

BigM = 2**64


class SimplexConstraintType(Enum):
    LEQ = 1
    EQ = 2
    GEQ = 3


class SimplexConstraint(NamedTuple):
    type_: SimplexConstraintType
    lhs: tuple[int, ...]
    rhs: int


@dataclass
class SimplexTableauRow:
    lhs: list[Fraction]
    rhs: Fraction

    def pad_lhs(self, size: int, value: Fraction = Fraction(0)) -> None:
        while len(self.lhs) < size:
            self.lhs.append(value)

    def __mul__(self, other: Fraction) -> "SimplexTableauRow":
        lhs = [x * other for x in self.lhs]
        rhs = self.rhs * other
        return SimplexTableauRow(lhs, rhs)

    def __rmul__(self, other: Fraction) -> "SimplexTableauRow":
        return self.__mul__(other)

    def __isub__(self, other: "SimplexTableauRow") -> "SimplexTableauRow":
        min_len = min(len(self.lhs), len(other.lhs))
        for i in range(0, min_len):
            self.lhs[i] -= other.lhs[i]
        self.rhs -= other.rhs
        return self

    def __itruediv__(self, other: Fraction) -> "SimplexTableauRow":
        for i in range(0, len(self.lhs)):
            self.lhs[i] /= other
        self.rhs /= other
        return self


class SimplexTableau:
    def __init__(self, profit: tuple[int, ...], constraints: Iterable[SimplexConstraint]) -> None:
        self.__profit: list[Fraction] = [Fraction(x) for x in profit]
        self.__var_count = len(profit)
        self.__constraints: list[SimplexTableauRow] = []
        self.__basic_variables: list[int] = []
        self.__column_count: int = len(profit)

        self.__build_rows(constraints)

    def __build_rows(self, constraints: Iterable[SimplexConstraint]) -> None:
        self.__constraints = []
        for constraint in constraints:
            match constraint.type_:
                case SimplexConstraintType.LEQ:
                    self.__addLEqConsraint(constraint.lhs, constraint.rhs)
                case SimplexConstraintType.EQ:
                    self.__addEqConsraint(constraint.lhs, constraint.rhs)
                case SimplexConstraintType.GEQ:
                    self.__addGEqConsraint(constraint.lhs, constraint.rhs)

    def __addLEqConsraint(self, lhs: tuple[int, ...], rhs: int) -> None:
        assert len(lhs) == self.__var_count
        new_lhs = [Fraction(x) for x in lhs]
        new_lhs.extend([Fraction(0) for _ in range(0, self.__column_count - len(lhs))])
        new_lhs.append(Fraction(1))
        new_row = SimplexTableauRow(lhs=new_lhs, rhs=Fraction(rhs))

        self.__column_count += 1

        self.__profit.append(Fraction(0))
        self.__basic_variables.append(self.__column_count - 1)

        for row in self.__constraints:
            row.pad_lhs(self.__column_count)
        self.__constraints.append(new_row)

    def __addEqConsraint(self, lhs: tuple[int, ...], rhs: int) -> None:
        assert len(lhs) == self.__var_count

        new_lhs = [Fraction(x) for x in lhs]
        new_lhs.extend([Fraction(0) for _ in range(0, self.__column_count - len(lhs))])
        new_lhs.append(Fraction(1))
        new_row = SimplexTableauRow(lhs=new_lhs, rhs=Fraction(rhs))

        self.__column_count += 1

        self.__profit.append(Fraction(-BigM))
        self.__basic_variables.append(self.__column_count - 1)

        for row in self.__constraints:
            row.pad_lhs(self.__column_count)
        self.__constraints.append(new_row)

    def __addGEqConsraint(self, lhs: tuple[int, ...], rhs: int) -> None:
        assert len(lhs) == self.__var_count

        new_lhs = [Fraction(x) for x in lhs]
        new_lhs.extend([Fraction(0) for _ in range(0, self.__column_count - len(lhs))])
        new_lhs.append(Fraction(-1))
        new_lhs.append(Fraction(1))
        new_row = SimplexTableauRow(lhs=new_lhs, rhs=Fraction(rhs))

        self.__column_count += 2

        self.__profit.append(Fraction(0))
        self.__profit.append(Fraction(-BigM))
        self.__basic_variables.append(self.__column_count - 1)

        for row in self.__constraints:
            row.pad_lhs(self.__column_count)
        self.__constraints.append(new_row)

    @property
    def rows(self) -> list[SimplexTableauRow]:
        return self.__constraints

    @property
    def zj(self) -> SimplexTableauRow:
        lhs: list[Fraction] = []
        for column_idx in range(0, self.__column_count):
            z = Fraction()
            for row_idx in range(0, len(self.__constraints)):
                idx = self.__basic_variables[row_idx]
                value = self.__constraints[row_idx].lhs[column_idx] * self.__profit[idx]
                z += value
            lhs.append(z)

        rhs = Fraction()
        for row_idx in range(0, len(self.__constraints)):
            idx = self.__basic_variables[row_idx]
            value = self.__constraints[row_idx].rhs * self.__profit[idx]
            rhs += value
        return SimplexTableauRow(lhs, rhs)

    @property
    def net_evaluation(self) -> list[Fraction]:
        return [x - y for x, y in zip(self.__profit, self.zj.lhs)]

    def set_basic_variable(self, row: int, idx: int) -> None:
        self.__basic_variables[row] = idx

    def get_solution(self) -> tuple[Fraction, tuple[Fraction, ...]]:  # Optimal Value, (x1, x2, ...)
        variables = [Fraction()] * self.__var_count
        for i, basic_var in enumerate(self.__basic_variables):
            if basic_var < self.__var_count:
                variables[basic_var] = self.__constraints[i].rhs
        return self.zj.rhs, tuple(variables)

    def __str__(self) -> str:
        result = ""
        result += f"    {' '.join(map(str, self.__profit))}\n"
        for i, row in enumerate(self.__constraints):
            result += f"{self.__basic_variables[i]} | {' '.join(map(str, row.lhs))} | {str(row.rhs)}\n"
        result += f"    {' '.join(map(str, self.zj.lhs))} | {str(self.zj.rhs)}\n"
        result += f"    {' '.join(map(str, self.net_evaluation))}\n"
        return result


class Simplex:
    def __init__(self, profit: tuple[int, ...]) -> None:
        self.__profit: tuple[int, ...] = profit
        self.__constraints: list[SimplexConstraint] = []
        self.__branch_and_bound_constraints: list[SimplexConstraint] = []

    @property
    def profit(self) -> tuple[int, ...]:
        return self.__profit

    @property
    def constraints(self) -> list[SimplexConstraint]:
        return self.__constraints

    def addLEqConsraint(self, lhs: list[int], rhs: int) -> None:
        new_constraint = SimplexConstraint(type_=SimplexConstraintType.LEQ, lhs=tuple(lhs), rhs=rhs)
        self.__constraints.append(new_constraint)

    def addEqConsraint(self, lhs: list[int], rhs: int) -> None:
        new_constraint = SimplexConstraint(type_=SimplexConstraintType.EQ, lhs=tuple(lhs), rhs=rhs)
        self.__constraints.append(new_constraint)

    def addGEqConsraint(self, lhs: list[int], rhs: int) -> None:
        new_constraint = SimplexConstraint(type_=SimplexConstraintType.GEQ, lhs=tuple(lhs), rhs=rhs)
        self.__constraints.append(new_constraint)

    def __find_pivot_column(self, tableau: SimplexTableau) -> int | None:
        pivot_column: int = -1
        max_value: Fraction = Fraction(0)
        for i, net_profit in enumerate(tableau.net_evaluation):
            if net_profit > 0 and net_profit > max_value:
                pivot_column = i
                max_value = net_profit
        return pivot_column if pivot_column >= 0 else None

    def __find_pivot_row(self, tableau: SimplexTableau, pivot_column: int) -> int | None:
        pivot_row = -1
        min_value = BigM
        for i, row in enumerate(tableau.rows):
            divisor = tableau.rows[i].lhs[pivot_column]
            if divisor <= 0:
                continue

            ratio = row.rhs / divisor
            if ratio < min_value:
                pivot_row = i
                min_value = ratio

        return pivot_row if pivot_row >= 0 else None

    def solve(self) -> tuple[Fraction, tuple[Fraction, ...]] | None:
        tableau = SimplexTableau(self.__profit, self.__constraints + self.__branch_and_bound_constraints)

        while (pivot_column_idx := self.__find_pivot_column(tableau)) is not None:
            pivot_row_idx = self.__find_pivot_row(tableau, pivot_column_idx)
            if pivot_row_idx is None:
                return None  # Unbound

            # Replace Basic variable
            tableau.set_basic_variable(pivot_row_idx, pivot_column_idx)

            # Pivot the Row
            pivot_value: Fraction = tableau.rows[pivot_row_idx].lhs[pivot_column_idx]
            tableau.rows[pivot_row_idx] /= pivot_value

            # Pivot the Column
            for row_idx, row in enumerate(tableau.rows):
                if row_idx == pivot_row_idx:
                    continue
                factor = row.lhs[pivot_column_idx]
                row -= factor * tableau.rows[pivot_row_idx]

        return tableau.get_solution()

    def __find_branch_and_bound_constraints(
        self, variables: tuple[Fraction, ...]
    ) -> tuple[SimplexConstraint, SimplexConstraint] | None:
        max_idx = -1
        max_value = -BigM
        for i, value in enumerate(variables):
            if value.is_integer():
                continue

            if value > max_value:
                max_value = value
                max_idx = i

        if max_idx < 0:
            return None

        filter_var = tuple([int(x == max_idx) for x in range(0, len(variables))])
        new_constraint_floor = SimplexConstraint(SimplexConstraintType.LEQ, lhs=filter_var, rhs=floor(max_value))
        new_constraint_ceil = SimplexConstraint(SimplexConstraintType.GEQ, lhs=filter_var, rhs=ceil(max_value))
        return new_constraint_floor, new_constraint_ceil

    def solve_integer(self) -> tuple[Fraction, tuple[Fraction, ...]] | None:
        solve_result = self.solve()
        if solve_result is None:
            return None
        solution_value, variables = solve_result

        if all(x.is_integer() for x in variables):
            return solution_value, variables

        # Start Branch & Bound
        extra_constraints = self.__find_branch_and_bound_constraints(variables)
        assert extra_constraints is not None

        constraints_stack: list[list[SimplexConstraint]] = [[extra_constraints[1]], [extra_constraints[0]]]

        lower_bound: Fraction = Fraction(-BigM)
        lower_bound_solution: tuple[Fraction, ...] = ()
        while constraints_stack:
            self.__branch_and_bound_constraints = constraints_stack.pop()

            solve_result = self.solve()
            if solve_result is None:
                continue
            solution_value, variables = solve_result

            if solution_value <= lower_bound:
                continue

            if all(x.is_integer() for x in variables):
                lower_bound = solution_value
                lower_bound_solution = variables
            else:
                new_constraints = self.__find_branch_and_bound_constraints(variables)
                if new_constraints:
                    constraints_stack.append(self.__branch_and_bound_constraints + [new_constraints[1]])
                    constraints_stack.append(self.__branch_and_bound_constraints + [new_constraints[0]])

        self.__branch_and_bound_constraints = []
        return lower_bound, lower_bound_solution

    def __str__(self) -> str:
        result = ""
        result += f"{' '.join(map(str, self.__profit))} \n"
        for row in self.__constraints:
            result += f"{row.type_}: {' '.join(map(str, row.lhs))}| {row.rhs}\n"
        return result


IndicatorLigths = tuple[bool, ...]
Button = tuple[int, ...]
Joltages = tuple[int, ...]


class Machine(NamedTuple):
    lights: IndicatorLigths
    buttons: list[Button]
    joltages: Joltages

    def simulate_joltage_configuration(self, presses: tuple[int, ...]) -> Joltages:
        jolatages = [0] * len(self.joltages)
        for i, press_amount in enumerate(presses):
            for counter in self.buttons[i]:
                jolatages[counter] += press_amount
        return tuple(jolatages)


def read_file(file_name: Path) -> list[Machine]:
    result: list[Machine] = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            parts = line.split()
            lights = ()
            buttons = []
            joltage: Joltages = ()

            for part in parts:
                first_char = part[0]
                value = part[1:-1]
                if first_char == "[":
                    lights = tuple([c == "#" for c in value])
                elif first_char == "(":
                    button = tuple([int(x) for x in value.split(",")])
                    buttons.append(button)
                elif first_char == "{":
                    joltage = tuple([int(x) for x in value.split(",")])
                else:
                    print("Invalid machine")
                    exit(2)

            machine = Machine(lights, buttons, joltage)
            result.append(machine)
    return result


def press_button(lights: IndicatorLigths, button: Button) -> IndicatorLigths:
    result = list(lights)
    for wire in button:
        result[wire] = not result[wire]
    return tuple(result)


def find_initialization_procedure(machine: Machine) -> int:
    target_lights = machine[0]
    buttons = machine[1]

    light_size = len(machine[0])
    init_lights = tuple([False] * light_size)
    queue = deque([(init_lights, 0)])

    seen = set()
    while len(queue) > 0:
        lights, button_presses = queue.popleft()

        for button in buttons:
            new_lights = press_button(lights, button)

            if new_lights == target_lights:
                return button_presses + 1

            if new_lights in seen:
                continue
            seen.add(new_lights)

            queue.append((new_lights, button_presses + 1))

    return -1


def find_joltage_configuration(machine: Machine) -> int:
    button_count = len(machine.buttons)

    simplex = Simplex(tuple([-1] * button_count))

    for i, requirement in enumerate(machine.joltages):
        lhs = [int(i in b) for b in machine.buttons]
        simplex.addEqConsraint(lhs, requirement)

    solve_result = simplex.solve_integer()
    if solve_result is None:
        print(f"Unable to find joltage configuration for {machine}")
        return 0
    optimal_value, variables = solve_result

    variables = tuple([int(x) for x in variables])
    assert machine.simulate_joltage_configuration(variables) == machine.joltages
    return -1 * int(optimal_value)


def run_initialization_procedures(machines: list[Machine]) -> int:
    with Pool() as thread_pool:
        return sum(thread_pool.imap(find_initialization_procedure, machines))


def run_joltage_configuration(machines: list[Machine]) -> int:
    with Pool() as thread_pool:
        return sum(thread_pool.imap(find_joltage_configuration, machines))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    machines = read_file(Path(sys.argv[1]))

    x = run_initialization_procedures(machines)
    print(f"Phase 1: {x}")

    x = run_joltage_configuration(machines)
    print(f"Phase 2: {x}")
