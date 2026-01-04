import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

Connections = dict[str, list[str]]

END_DEVICE = "out"


def read_file(file_name: Path) -> Connections:
    connections = {}
    with open(file_name) as f:
        for line in f.read().splitlines():
            device, successors = line.split(":")
            connections[device] = successors.split()
    return connections


def count_traces(connections: Connections, start: str) -> int:
    current_devices: defaultdict[str, int] = defaultdict(int)
    current_devices[start] = 1

    while len(current_devices) > 1 or END_DEVICE not in current_devices:
        next_devices: defaultdict[str, int] = defaultdict(int)

        for current_device, trace_count in current_devices.items():
            if current_device == END_DEVICE:
                next_devices[END_DEVICE] += trace_count
                continue

            for successor in connections[current_device]:
                next_devices[successor] += trace_count

        current_devices = next_devices

    return current_devices[END_DEVICE]


@dataclass
class TraceState:
    trace_count: int
    dac_trace_count: int
    fft_trace_count: int
    critical_trace_count: int

    def __add__(self, other: "TraceState") -> "TraceState":
        return TraceState(
            trace_count=self.trace_count + other.trace_count,
            dac_trace_count=self.dac_trace_count + other.dac_trace_count,
            fft_trace_count=self.fft_trace_count + other.fft_trace_count,
            critical_trace_count=self.critical_trace_count + other.critical_trace_count,
        )

    @classmethod
    def zero(cls) -> "TraceState":
        return TraceState(trace_count=0, dac_trace_count=0, fft_trace_count=0, critical_trace_count=0)


def count_critical_traces(connections: Connections, start: str) -> int:
    current_devices: defaultdict[str, TraceState] = defaultdict(TraceState.zero)
    current_devices[start] = TraceState(trace_count=1, dac_trace_count=0, fft_trace_count=0, critical_trace_count=0)

    while len(current_devices) > 1 or END_DEVICE not in current_devices:
        next_devices: defaultdict[str, TraceState] = defaultdict(TraceState.zero)

        for current_device, current_trace_state in current_devices.items():
            if current_device == END_DEVICE:
                next_devices[END_DEVICE] += current_trace_state
                continue

            for successor in connections[current_device]:
                if successor == "dac":
                    adjustment_trace_count = current_trace_state.trace_count
                    adjustment_dac_trace_count = current_trace_state.trace_count - current_trace_state.fft_trace_count
                    adjustment_fft_trace_count = 0
                    adjustment_critical_trace_count = current_trace_state.fft_trace_count
                elif successor == "fft":
                    adjustment_trace_count = current_trace_state.trace_count
                    adjustment_dac_trace_count = 0
                    adjustment_fft_trace_count = current_trace_state.trace_count - current_trace_state.dac_trace_count
                    adjustment_critical_trace_count = current_trace_state.dac_trace_count
                else:
                    adjustment_trace_count = current_trace_state.trace_count
                    adjustment_dac_trace_count = current_trace_state.dac_trace_count
                    adjustment_fft_trace_count = current_trace_state.fft_trace_count
                    adjustment_critical_trace_count = current_trace_state.critical_trace_count

                adjustment_state = TraceState(
                    trace_count=adjustment_trace_count,
                    dac_trace_count=adjustment_dac_trace_count,
                    fft_trace_count=adjustment_fft_trace_count,
                    critical_trace_count=adjustment_critical_trace_count,
                )
                next_devices[successor] += adjustment_state

        current_devices = next_devices

    return current_devices[END_DEVICE].critical_trace_count


def main() -> None:
    if len(sys.argv) != 3:
        print("Please provide the input file and starting machine!", file=sys.stderr)
        exit(-1)

    file_path: str = sys.argv[1]
    start_device: str = sys.argv[2]

    connections = read_file(Path(file_path))

    count_all = count_traces(connections, start_device)
    print(f"Phase 1: {count_all}")

    count_critical = count_critical_traces(connections, start_device)
    print(f"Phase 2: {count_critical}")


if __name__ == "__main__":
    main()
