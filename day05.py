from collections.abc import Iterator
from hashlib import md5
from itertools import count, islice
from typing import Literal, cast

from aocd import get_data

type DoorID = str
type Digest = str
type Position = Literal[0, 1, 2, 3, 4, 5, 6, 7]
type PasswordChar = str
type Candidate = tuple[Position, PasswordChar]


def parse_input(input: str) -> DoorID:
    """Parse raw puzzle input into a door ID."""
    return input.strip()


def qualifying_digests(door_id: DoorID) -> Iterator[Digest]:
    """Yield MD5 hex digests that start with five zeroes."""
    for nonce in count():
        digest = md5(f"{door_id}{nonce}".encode()).hexdigest()
        if digest.startswith("00000"):
            yield digest


def part1_chars(door_id: DoorID) -> Iterator[PasswordChar]:
    """Yield the next password characters for part 1."""
    for digest in qualifying_digests(door_id):
        yield digest[5]


def part1(door_id: DoorID) -> str:
    """Compute the part 1 password."""
    return "".join(islice(part1_chars(door_id), 8))


def part2_candidates(door_id: DoorID) -> Iterator[Candidate]:
    """Yield (position, character) candidates for the part 2 password."""
    for digest in qualifying_digests(door_id):
        pos_char = digest[5]
        if pos_char.isdigit():
            pos_int = int(pos_char)
            if 0 <= pos_int < 8:
                yield cast(Position, pos_int), digest[6]


def part2(door_id: DoorID) -> str:
    """Compute the part 2 password."""
    password: dict[Position, PasswordChar] = {}
    for pos, c in part2_candidates(door_id):
        if pos not in password:
            password[pos] = c
        if len(password) == 8:
            break
    return "".join(c for _, c in sorted(password.items()))


def main() -> None:
    """Solve and print both parts of the puzzle."""
    data: str = get_data(year=2016, day=5)
    door_id = parse_input(data)

    print(f"Part 1: {part1(door_id)}")
    print(f"Part 2: {part2(door_id)}")


if __name__ == "__main__":
    main()
