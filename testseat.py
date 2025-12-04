"""Simple seating randomizer for exams.

- Defaults to load students from `logic.txt` (UTF-8), lines like: `<id><tab/space><name>`.
- Run `python testseat.py` to print the assignment list and a grid view.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class Seat:
    row: int
    col: int

    def label(self) -> str:
        return f"R{self.row}C{self.col}"


def load_students(path: Path) -> List[str]:
    """Load students from a UTF-8 text file containing `<id> <name>` per line."""
    students: List[str] = []
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            student_id = parts[0]
            name = "".join(parts[1:])
            students.append(f"{student_id} {name}")
        else:
            students.append(parts[0])
    return students


def assign_seats(
    students: Sequence[str],
    rows: int,
    cols: int,
    blocked: Iterable[Tuple[int, int]] | None = None,
    seed: int | None = None,
) -> List[Tuple[Seat, str]]:
    """Randomly assign students to seats."""
    blocked_set = {Seat(r, c) for r, c in (blocked or [])}
    all_seats = [Seat(r, c) for r in range(1, rows + 1) for c in range(1, cols + 1)]
    available_seats = [s for s in all_seats if s not in blocked_set]

    if len(students) > len(available_seats):
        raise ValueError("Not enough available seats for all students.")

    rng = random.Random(seed)
    shuffled = list(students)
    rng.shuffle(shuffled)

    return list(zip(available_seats, shuffled))


def format_grid(assignments: List[Tuple[Seat, str]], rows: int, cols: int) -> str:
    """Return a string grid showing seat labels and names."""
    grid = [["" for _ in range(cols)] for _ in range(rows)]
    for seat, student in assignments:
        grid[seat.row - 1][seat.col - 1] = student
    lines = []
    for r, row in enumerate(grid, start=1):
        cells = []
        for c, name in enumerate(row, start=1):
            label = f"R{r}C{c}"
            display = name or "-"
            cells.append(f"{label}: {display}")
        lines.append(" | ".join(cells))
    return "\n".join(lines)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    students_file = Path("logic.txt")
    if students_file.exists():
        students = load_students(students_file)
    else:
        # Fallback demo list.
        students = [
            "Alice",
            "Bob",
            "Charlie",
            "Dana",
            "Eli",
            "Fatima",
            "Gina",
            "Hiro",
            "Ivy",
            "Jamal",
            "Kim",
            "Liu",
        ]

    # Adjust to your classroom layout. 7x9 fits the 63 students in logic.txt.
    rows = 7
    cols = 9
    blocked_seats: list[tuple[int, int]] = [
        # (row, col),
    ]
    seed = None  # Set an int (e.g., 42) to reproduce the same shuffle.

    assignments = assign_seats(students, rows, cols, blocked=blocked_seats, seed=seed)

    print("Seating assignments:")
    for seat, student in assignments:
        print(f"{seat.label()}: {student}")

    print("\nRoom view:")
    print(format_grid(assignments, rows, cols))


if __name__ == "__main__":
    main()


# python -m http.server 8000
# Then open http://localhost:8000/testseat.py in a browser to see the output.
# http://localhost:8000/index.html for a simple file listing.