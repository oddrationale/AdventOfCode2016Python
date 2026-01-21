from itertools import batched

from aocd import get_data

type Specification = tuple[int, int, int]
type Specifications = tuple[Specification, ...]


def parse_input(input: str) -> Specifications:
    """Parse input string into tuple of triangle specifications."""
    return tuple(
        (int(a), int(b), int(c))
        for a, b, c in (line.split() for line in input.splitlines())
    )


def is_valid_triangle(spec: Specification) -> bool:
    """Check if three sides can form a valid triangle."""
    a, b, c = spec
    return a + b > c and a + c > b and b + c > a


def part1(specs: Specifications) -> int:
    """Count valid triangles from row-based specifications."""
    return sum(is_valid_triangle(spec) for spec in specs)


def transform_by_columns(specs: Specifications) -> Specifications:
    """Transform specifications by reading values column-wise instead of row-wise."""
    col1: tuple[int, ...] = tuple(a for a, _, _ in specs)
    col2: tuple[int, ...] = tuple(b for _, b, _ in specs)
    col3: tuple[int, ...] = tuple(c for _, _, c in specs)
    combined: tuple[int, ...] = col1 + col2 + col3
    return tuple(tuple(batch) for batch in batched(combined, 3))


def part2(specs: Specifications) -> int:
    """Count valid triangles from column-based specifications."""
    transformed: Specifications = transform_by_columns(specs)
    return sum(is_valid_triangle(spec) for spec in transformed)


def main() -> None:
    """Solve and print both parts of the puzzle."""
    data: str = get_data(year=2016, day=3)
    specs: Specifications = parse_input(data)

    print(f"Part 1: {part1(specs)}")
    print(f"Part 2: {part2(specs)}")


if __name__ == "__main__":
    main()
