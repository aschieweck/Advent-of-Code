import cProfile
import re
import sys


def read_file(file_name: str) -> list[tuple[int, int]]:
    result = []
    with open(file_name) as f:
        content = f.read().splitlines()[0]
        id_ranges = content.split(",")
        for id_range in id_ranges:
            ids = id_range.split("-")
            id1 = int(ids[0])
            id2 = int(ids[1])
            result.append((id1, id2))
    return result


def check_ids(id_ranges: list[tuple[int, int]]) -> int:
    result = 0

    for id_range in id_ranges:
        id1, id2 = id_range

        for i in range(id1, id2 + 1):
            i_str = str(i)
            split_idx = len(i_str) // 2
            if i_str[:split_idx] == i_str[split_idx:]:
                result += i

    return result


def check_ids_regex(id_ranges: list[tuple[int, int]]) -> int:
    result = 0

    regex = re.compile(r'^(\d+)\1$')

    for id_range in id_ranges:
        id1, id2 = id_range

        for i in range(id1, id2 + 1):
            i_str = str(i)

            if regex.match(i_str):
                result += i

    return result


def check_ids_2(id_ranges: list[tuple[int, int]]) -> int:
    result = 0

    for id_range in id_ranges:
        id1, id2 = id_range

        for i in range(id1, id2 + 1):
            i_str = str(i)

            for j in range(1, len(i_str) // 2 + 1):
                chunks = [i_str[k:k + j] for k in range(0, len(i_str), j)]
                if len(set(chunks)) == 1:
                    result += i
                    # early exit of chunking as it's an silly id already
                    break

    return result


def check_ids_2_regex(id_ranges: list[tuple[int, int]]) -> int:
    result = 0

    regex = re.compile(r'^(\d+)\1+$')

    for id_range in id_ranges:
        id1, id2 = id_range

        for i in range(id1, id2 + 1):
            i_str = str(i)

            if regex.match(i_str):
                result += i

    return result


def profile_and_run(label, func, arg):
    profiler = cProfile.Profile()
    profiler.enable()
    retval = func(arg)
    profiler.disable()
    print(f"{label}:\t", retval)
    profiler.print_stats()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    input = read_file(sys.argv[1])

    profile_and_run("Phase 1", check_ids, input)
    profile_and_run("Phase 1 (regex)", check_ids_regex, input)
    profile_and_run("Phase 2", check_ids_2, input)
    profile_and_run("Phase 2 (regex)", check_ids_2_regex, input)
