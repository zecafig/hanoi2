import pytest

from hanoi.core import HanoiGame, PieceCountPrompt


def test_initial_game_state() -> None:
    game = HanoiGame(4)

    assert game.piece_count == 4
    assert game.towers == [[4, 3, 2, 1], [], []]
    assert game.selected_tower is None
    assert game.move_count == 0
    assert not game.has_won


def test_piece_count_validation() -> None:
    with pytest.raises(ValueError):
        HanoiGame(0)

    with pytest.raises(ValueError):
        HanoiGame(13)


def test_select_and_move_disk() -> None:
    game = HanoiGame(3)

    first_pick = game.select_or_move(0)
    move = game.select_or_move(1)

    assert first_pick == "selected"
    assert move == "moved"
    assert game.towers == [[3, 2], [1], []]
    assert game.selected_tower is None
    assert game.move_count == 1


def test_invalid_move_is_rejected_and_selection_stays() -> None:
    game = HanoiGame(3)

    game.select_or_move(0)
    game.select_or_move(1)
    game.select_or_move(0)
    result = game.select_or_move(1)

    assert result == "invalid"
    assert game.towers == [[3, 2], [1], []]
    assert game.selected_tower == 0
    assert game.move_count == 1


def test_win_detection() -> None:
    game = HanoiGame(1)

    game.select_or_move(0)
    game.select_or_move(2)

    assert game.has_won


def test_middle_tower_is_not_a_win() -> None:
    game = HanoiGame(1)

    game.select_or_move(0)
    game.select_or_move(1)

    assert not game.has_won


def test_reset_current_game() -> None:
    game = HanoiGame(3)

    game.select_or_move(0)
    game.select_or_move(2)
    game.reset()

    assert game.towers == [[3, 2, 1], [], []]
    assert game.selected_tower is None
    assert game.move_count == 0


def test_new_game_changes_piece_count() -> None:
    game = HanoiGame(3)

    game.start_new_game(5)

    assert game.piece_count == 5
    assert game.towers == [[5, 4, 3, 2, 1], [], []]


def test_cursor_navigation_wraps() -> None:
    game = HanoiGame(3)

    assert game.cursor_tower == 0
    game.move_cursor(-1)
    assert game.cursor_tower == 2
    game.move_cursor(1)
    assert game.cursor_tower == 0


def test_prompt_accepts_digits_backspace_and_enter() -> None:
    prompt = PieceCountPrompt(min_count=1, max_count=12)

    assert prompt.apply_key("1") is None
    assert prompt.apply_key("2") is None
    assert prompt.text == "12"

    assert prompt.apply_key("BACKSPACE") is None
    assert prompt.text == "1"

    assert prompt.apply_key("ENTER") == 1


def test_prompt_rejects_out_of_range_and_sets_error() -> None:
    prompt = PieceCountPrompt(min_count=1, max_count=12)

    prompt.apply_key("0")
    result = prompt.apply_key("ENTER")

    assert result is None
    assert prompt.error == "Enter a value between 1 and 12."


def test_prompt_rejects_empty_enter() -> None:
    prompt = PieceCountPrompt(min_count=1, max_count=12)

    result = prompt.apply_key("ENTER")

    assert result is None
    assert prompt.error == "Enter a value between 1 and 12."


def test_prompt_ignores_non_digit_and_clear_works() -> None:
    prompt = PieceCountPrompt(min_count=1, max_count=12)

    prompt.apply_key("A")
    assert prompt.text == ""

    prompt.apply_key("3")
    prompt.clear()
    assert prompt.text == ""
    assert prompt.error is None


def test_selecting_empty_tower_returns_empty() -> None:
    game = HanoiGame(3)

    assert game.select_or_move(1) == "empty"


def test_selecting_same_tower_twice_deselects() -> None:
    game = HanoiGame(3)

    game.select_or_move(0)
    result = game.select_or_move(0)

    assert result == "deselected"
    assert game.selected_tower is None


def test_invalid_tower_index_raises() -> None:
    game = HanoiGame(3)

    with pytest.raises(ValueError):
        game.select_or_move(-1)

    with pytest.raises(ValueError):
        game.select_or_move(3)


def test_optimal_moves_formula() -> None:
    game = HanoiGame(4)

    assert game.get_optimal_moves() == 15


def test_solver_generates_optimal_winning_sequence() -> None:
    game = HanoiGame(3)

    moves = game.solve()

    assert len(moves) == game.get_optimal_moves()

    for source, target in moves:
        game.select_or_move(source)
        result = game.select_or_move(target)
        assert result == "moved"

    assert game.has_won
