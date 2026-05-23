"""Core game state and input helpers for Tower of Hanoi."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PieceCountPrompt:
    """Tracks piece-count text entry for new and initial games."""

    min_count: int = 1
    max_count: int = 12
    text: str = ""
    error: str | None = None

    def apply_key(self, key: str) -> int | None:
        normalized = key.upper()

        if normalized.isdigit() and len(normalized) == 1:
            if len(self.text) < 2:
                self.text += normalized
            self.error = None
            return None

        if normalized == "BACKSPACE":
            self.text = self.text[:-1]
            self.error = None
            return None

        if normalized == "ENTER":
            if not self.text:
                self.error = f"Enter a value between {self.min_count} and {self.max_count}."
                return None
            value = int(self.text)
            if self.min_count <= value <= self.max_count:
                self.error = None
                return value
            self.error = f"Enter a value between {self.min_count} and {self.max_count}."
            return None

        return None

    def clear(self) -> None:
        self.text = ""
        self.error = None


class HanoiGame:
    """Mutable Tower of Hanoi board state and movement rules."""

    min_count = 1
    max_count = 12

    def __init__(self, piece_count: int) -> None:
        self._validate_piece_count(piece_count)
        self.piece_count = piece_count
        self.towers: list[list[int]] = [[], [], []]
        self.selected_tower: int | None = None
        self.cursor_tower = 0
        self.move_count = 0
        self.reset()

    def _validate_piece_count(self, piece_count: int) -> None:
        if piece_count < self.min_count or piece_count > self.max_count:
            raise ValueError(
                f"piece_count must be between {self.min_count} and {self.max_count}, got {piece_count}"
            )

    @property
    def has_won(self) -> bool:
        target = list(range(self.piece_count, 0, -1))
        return self.towers[2] == target

    def reset(self) -> None:
        self.towers = [list(range(self.piece_count, 0, -1)), [], []]
        self.selected_tower = None
        self.cursor_tower = 0
        self.move_count = 0

    def start_new_game(self, piece_count: int) -> None:
        self._validate_piece_count(piece_count)
        self.piece_count = piece_count
        self.reset()

    def move_cursor(self, delta: int) -> None:
        self.cursor_tower = (self.cursor_tower + delta) % 3

    def select_or_move(self, tower_index: int) -> str:
        if tower_index < 0 or tower_index > 2:
            raise ValueError("tower_index must be 0, 1, or 2")

        if self.selected_tower is None:
            if not self.towers[tower_index]:
                return "empty"
            self.selected_tower = tower_index
            return "selected"

        if self.selected_tower == tower_index:
            self.selected_tower = None
            return "deselected"

        source = self.towers[self.selected_tower]
        target = self.towers[tower_index]
        moving_piece = source[-1]

        if target and target[-1] < moving_piece:
            return "invalid"

        target.append(source.pop())
        self.selected_tower = None
        self.move_count += 1
        return "moved"

    def get_optimal_moves(self) -> int:
        return (2**self.piece_count) - 1

    def solve(self) -> list[tuple[int, int]]:
        moves: list[tuple[int, int]] = []

        def _hanoi(n: int, source: int, destination: int, auxiliary: int) -> None:
            if n == 1:
                moves.append((source, destination))
                return
            _hanoi(n - 1, source, auxiliary, destination)
            moves.append((source, destination))
            _hanoi(n - 1, auxiliary, destination, source)

        _hanoi(self.piece_count, 0, 2, 1)
        return moves
