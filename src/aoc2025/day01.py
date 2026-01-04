import sys


def read_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.read().splitlines()


def find_password(inputs: list[str]) -> int:
    password = 0
    dial_position = 50

    for line in inputs:
        direction = line[0]
        clicks = int(line[1:])

        if direction == 'L':
            dial_position = dial_position - clicks
        else:
            dial_position = dial_position + clicks
        dial_position = dial_position % 100

        if dial_position == 0:
            password = password + 1

    return password


def find_password_2(inputs: list[str]) -> int:
    password = 0
    dial_position = 50

    for line in inputs:
        direction = line[0]
        clicks = int(line[1:])

        if direction == 'L':
            dial_position_mirrored = (100 - dial_position) % 100
            password += (dial_position_mirrored + clicks) // 100
            dial_position = (dial_position - clicks) % 100
        else:
            password += (dial_position + clicks) // 100
            dial_position = (dial_position + clicks) % 100

    return password


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    inputs = read_file(sys.argv[1])

    print("Phase 1:", find_password(inputs))
    print("Phase 2:", find_password_2(inputs))
