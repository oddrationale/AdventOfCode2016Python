from aocd import get_data


def parse_input(input: str): ...


def part1(): ...


def part2(): ...


def main() -> None:
    """Solve and print both parts of the puzzle."""
    data: str = get_data(year=2016, day=1)
    parse_input(data)

    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


if __name__ == "__main__":
    main()
