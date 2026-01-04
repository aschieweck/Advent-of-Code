import sys


def read_file(file_name: str) -> list[list[int]]:
    result = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            line_as_int_array = [int(digit) for digit in line]
            result += [line_as_int_array]

    return result


def find_max(array: list[int], start: int, end: int) -> tuple[int, int]:
    max_value = -1
    idx = -1
    for i in range(start, end):
        value = array[i]
        if value > max_value:
            max_value = value
            idx = i

    return max_value, idx


def max_joltage(banks: list[list[int]], battery_amount: int = 2) -> int:
    result = 0
    for bank in banks:
        bank_joltage = 0
        current_idx = 0
        for end_idx in range(len(bank) - battery_amount, len(bank)):
            joltage, current_idx = find_max(bank, current_idx, end_idx + 1)

            bank_joltage = 10 * bank_joltage + joltage
            current_idx += 1

        result += bank_joltage

    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    banks = read_file(sys.argv[1])

    print("Phase 1:", max_joltage(banks,  2))
    print("Phase 2:", max_joltage(banks, 12))
