import sys


def check_ids(file_name: str) -> int:
    result = 0

    with open(file_name) as f:
        line = f.readline().strip()
        id_ranges = line.split(",")

        for id_range in id_ranges:
            ids = id_range.split("-")
            id1 = int(ids[0])
            id2 = int(ids[1])

            for i in range(id1, id2 + 1):
                i_str = str(i)
                split_idx = len(i_str) // 2
                if i_str[:split_idx] == i_str[split_idx:]:
                    result += i

    return result


def check_ids_2(file_name: str) -> int:
    result = 0

    with open(file_name) as f:
        line = f.readline().strip()
        id_ranges = line.split(",")

        for id_range in id_ranges:
            ids = id_range.split("-")
            id1 = int(ids[0])
            id2 = int(ids[1])

            for i in range(id1, id2 + 1):
                i_str = str(i)

                for j in range(1, len(i_str) // 2 + 1):
                    chunks = [i_str[k:k + j] for k in range(0, len(i_str), j)]
                    if len(set(chunks)) == 1:
                        result += i
                        # early exit of chunking as it's an silly id already
                        break
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    print("Phase 1:", check_ids(sys.argv[1]))
    print("Phase 2:", check_ids_2(sys.argv[1]))
