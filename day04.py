import re
from collections import Counter
from dataclasses import dataclass
from typing import Self

from aocd import get_data

ORD_A: int = ord("a")
ALPHABET_SIZE: int = 26


@dataclass(frozen=True, slots=True)
class Room:
    """An encrypted room with a sector ID and checksum."""

    encrypted_name: str
    sector_id: int
    checksum: str

    @classmethod
    def from_string(cls, s: str) -> Self | None:
        """Parse a room from its string representation, or None if invalid."""
        if m := re.match(pattern=r"([a-z-]+)-(\d+)\[([a-z]+)\]", string=s):
            return cls(
                encrypted_name=m.group(1),
                sector_id=int(m.group(2)),
                checksum=m.group(3),
            )


type Rooms = tuple[Room, ...]


def parse_input(input: str) -> Rooms:
    """Parse the puzzle input into a tuple of rooms."""
    return tuple(filter(None, (Room.from_string(line) for line in input.splitlines())))


def is_real(room: Room) -> bool:
    """Return True if the room's checksum matches its letter frequencies."""
    counts = Counter(room.encrypted_name.replace("-", ""))
    checksum: str = "".join(
        k for k, _ in sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:5]
    )
    return checksum == room.checksum


def part1(rooms: Rooms) -> int:
    """Return the sum of sector IDs of all real rooms."""
    return sum(room.sector_id for room in filter(is_real, rooms))


def decrypt(room: Room) -> str:
    """Decrypt the room name using a Caesar cipher shifted by the sector ID."""
    return "".join(
        chr(
            (((ord(c) - ORD_A) + (room.sector_id % ALPHABET_SIZE)) % ALPHABET_SIZE)
            + ORD_A
        )
        if c != "-"
        else " "
        for c in room.encrypted_name
    )


def part2(rooms: Rooms) -> int | None:
    """Return the sector ID of the room where North Pole objects are stored."""
    for room in rooms:
        if is_real(room):
            decrypted_name = decrypt(room)
            if "northpole" in decrypted_name:
                return room.sector_id
    return None


def main() -> None:
    """Solve and print both parts of the puzzle."""
    data: str = get_data(year=2016, day=4)
    rooms = parse_input(input=data)

    print(f"Part 1: {part1(rooms)}")
    print(f"Part 2: {part2(rooms)}")


if __name__ == "__main__":
    main()
