from collections.abc import Iterator
from enum import Enum, StrEnum
from functools import reduce
from typing import NamedTuple

from aocd import get_data


class Orientation(Enum):
    """Cardinal directions (North, East, South, West)."""

    N = "N"
    E = "E"
    S = "S"
    W = "W"


class Position(NamedTuple):
    """2D coordinate position."""

    x: int
    y: int


type State = tuple[Position, Orientation]
"""A tuple representing the current position and orientation."""


class Rotation(StrEnum):
    """Turn direction (Left or Right)."""

    L = "L"
    R = "R"


class Instruction(NamedTuple):
    """A turn direction and distance to walk."""

    rotation: Rotation
    distance: int


DIRECTIONS = {
    Orientation.N: (0, 1),
    Orientation.E: (1, 0),
    Orientation.S: (0, -1),
    Orientation.W: (-1, 0),
}
TURN_RIGHT: dict[Orientation, Orientation] = {
    Orientation.N: Orientation.E,
    Orientation.E: Orientation.S,
    Orientation.S: Orientation.W,
    Orientation.W: Orientation.N,
}
TURN_LEFT: dict[Orientation, Orientation] = {
    Orientation.N: Orientation.W,
    Orientation.W: Orientation.S,
    Orientation.S: Orientation.E,
    Orientation.E: Orientation.N,
}


def parse_input(input: str) -> list[Instruction]:
    """Parse the input into a list of instructions."""
    return [Instruction(Rotation(i[0]), int(i[1:])) for i in input.split(", ")]


def turn(orientation: Orientation, rotation: Rotation) -> Orientation:
    """Return new orientation after turning left or right."""
    if rotation == Rotation.R:
        return TURN_RIGHT[orientation]
    else:
        return TURN_LEFT[orientation]


def move(current: State, instruction: Instruction) -> State:
    """Execute a single instruction and return new position and orientation."""
    current_position, current_orientation = current
    rotation, distance = instruction
    new_orientation = turn(current_orientation, rotation)
    dx, dy = DIRECTIONS[new_orientation]

    return Position(
        current_position.x + dx * distance,
        current_position.y + dy * distance,
    ), new_orientation


def part1(instructions: list[Instruction]) -> int:
    """Calculate Manhattan distance to final position."""
    final_position, _ = reduce(
        move,
        instructions,
        (Position(0, 0), Orientation.N),
    )
    return abs(final_position.x) + abs(final_position.y)


def generate_all_positions(
    start: State,
    instructions: list[Instruction],
) -> Iterator[Position]:
    """Generate all positions visited while following instructions."""
    current_position, current_orientation = start
    yield current_position

    for instruction in instructions:
        rotation, distance = instruction
        current_orientation = turn(current_orientation, rotation)
        dx, dy = DIRECTIONS[current_orientation]
        for _ in range(distance):
            current_position = Position(
                current_position.x + dx,
                current_position.y + dy,
            )
            yield current_position


def part2(instructions: list[Instruction]) -> int:
    """Find the first location visited twice."""
    all_positions = generate_all_positions(
        (Position(0, 0), Orientation.N),
        instructions,
    )
    seen: set[Position] = set()
    for pos in all_positions:
        if pos in seen:
            return abs(pos.x) + abs(pos.y)
        seen.add(pos)
    return 0


def main() -> None:
    """Solve and print both parts of the puzzle."""
    data = get_data(year=2016, day=1)
    instructions = parse_input(data)

    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")


if __name__ == "__main__":
    main()
