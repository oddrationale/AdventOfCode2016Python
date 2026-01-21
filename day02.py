from dataclasses import dataclass
from enum import StrEnum
from functools import reduce
from itertools import accumulate

from aocd import get_data


class Direction(StrEnum):
    """Valid movement directions on a keypad."""

    U = "U"
    D = "D"
    L = "L"
    R = "R"


type Position = tuple[int, int]
type Keypad = dict[Position, str]
type Instruction = tuple[Direction, ...]
type Instructions = tuple[Instruction, ...]

MOVEMENT: dict[Direction, Position] = {
    Direction.U: (0, -1),
    Direction.D: (0, 1),
    Direction.L: (-1, 0),
    Direction.R: (1, 0),
}

# fmt: off
STANDARD_KEYPAD: Keypad = {
    (0, 0): "1", (1, 0): "2", (2, 0): "3",
    (0, 1): "4", (1, 1): "5", (2, 1): "6",
    (0, 2): "7", (1, 2): "8", (2, 2): "9",
}

DIAMOND_KEYPAD: Keypad = {
                              (2, 0): "1",
                 (1, 1): "2", (2, 1): "3", (3, 1): "4",
    (0, 2): "5", (1, 2): "6", (2, 2): "7", (3, 2): "8", (4, 2): "9",
                 (1, 3): "A", (2, 3): "B", (3, 3): "C",
                              (2, 4): "D",
}
# fmt: on


@dataclass(frozen=True, slots=True)
class KeypadConfig:
    """Configuration for a keypad layout with validated start position.

    Attributes:
        keypad: Mapping from positions to button labels.
        start: Initial position (must exist in keypad).

    Raises:
        ValueError: If start position is not in the keypad.
    """

    keypad: Keypad
    start: Position

    def __post_init__(self) -> None:
        if self.start not in self.keypad:
            raise ValueError(f"Start position {self.start} not in keypad")


STANDARD = KeypadConfig(STANDARD_KEYPAD, (1, 1))
DIAMOND = KeypadConfig(DIAMOND_KEYPAD, (0, 2))


def parse_input(input: str) -> Instructions:
    """Parse input into a sequence of movement instructions."""
    return tuple(tuple(Direction(c) for c in line) for line in input.splitlines())


def step(state: Position, direction: Direction, keypad: Keypad) -> Position:
    """Move one step in a direction if the new position is valid."""
    x, y = state
    dx, dy = MOVEMENT[direction]
    nx, ny = x + dx, y + dy
    if (nx, ny) in keypad:
        return (nx, ny)
    return (x, y)


def next_button(state: Position, instruction: Instruction, keypad: Keypad) -> Position:
    """Execute a sequence of movements to find the next button."""
    return reduce(
        lambda s, d: step(s, d, keypad),
        instruction,
        state,
    )


def solve(instructions: Instructions, config: KeypadConfig) -> str:
    """Solve the bathroom code puzzle for a given keypad configuration."""

    def run_instruction(state: Position, instruction: Instruction) -> Position:
        return next_button(state, instruction, config.keypad)

    buttons: list[Position] = list(
        accumulate(
            instructions,
            run_instruction,
            initial=config.start,
        )
    )
    return "".join(config.keypad[pos] for pos in buttons[1:])


def part1(instructions: Instructions) -> str:
    """Solve Part 1 using the standard 3x3 numeric keypad."""
    return solve(instructions, STANDARD)


def part2(instructions: Instructions) -> str:
    """Solve Part 2 using the diamond-shaped keypad."""
    return solve(instructions, DIAMOND)


def main() -> None:
    """Solve and print both parts of the puzzle."""
    data: str = get_data(year=2016, day=2)
    instructions: Instructions = parse_input(data)

    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")


if __name__ == "__main__":
    main()
