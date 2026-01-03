import sys
from pathlib import Path
from typing import NamedTuple

class Problem(NamedTuple):
    operator: str
    numbers: list[int]


def read_file(file_name: Path) -> list[str]:
    result = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            result.append(line)
    return result


def parse_worksheet_phase1(content: list[str]) -> list[Problem]:
    columns = []
    for line in content:
        columns.append(line.split())

    problems = []
    for i in range(0, len(columns[0])):
        operator = columns[-1][i]
        numbers = [int(columns[j][i]) for j in range(0, len(columns) - 1)]
        problems.append(Problem(operator, numbers))
    return problems


def parse_worksheet_phase2(content: list[str]) -> list[Problem]:
    operators = content[-1].split()

    transposed_content = []
    for j in range(0, len(content[0])):
        number_str = ""
        for i in range(0, len(content) - 1):
            number_str += content[i][j]
        transposed_content.append(number_str)

    current_operator = 0
    current_numbers = []
    problems = []
    for line in transposed_content:
        if line.strip() == "":
            problems.append(Problem(operators[current_operator], current_numbers))
            current_operator += 1
            current_numbers = []
        else:
            current_numbers.append(int(line))
    problems.append(Problem(operators[current_operator], current_numbers))

    return problems


def product(factors: list[int]) -> int:
    result = 1
    for i in factors:
        result *= i
    return result


def calculate_problems(problems: list[Problem]) -> list[int]:
    result = []
    for problem in problems:
        problem_function = sum if problem.operator == "+" else product
        result.append(problem_function(problem.numbers))
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    content = read_file(Path(sys.argv[1]))

    problems1 = parse_worksheet_phase1(content)
    answers1 = calculate_problems(problems1)
    print("Phase 1:", sum(answers1))

    problems2 = parse_worksheet_phase2(content)
    answers2 = calculate_problems(problems2)
    print("Phase 2:", sum(answers2))
