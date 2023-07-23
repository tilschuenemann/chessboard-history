from pathlib import Path
from typing import List

import pytest

from src.chessboard_history.main import ChessboardHistory


@pytest.fixture
def tmp_dir(tmp_path) -> Path:
    d = Path(tmp_path / "tmp")
    d.mkdir()
    return d


@pytest.mark.parametrize(
    "values,exp,raiseError",
    [
        ([], [], False),
        (
            [
                0,
            ],
            [
                "00",
            ],
            False,
        ),
        ([256], ["00"], True),
        ([-1], ["x1"], True),
    ],
)
def test_hex_wrapper(values: List[int], exp: List[str], raiseError: bool) -> None:
    ch = ChessboardHistory()

    if raiseError:
        with pytest.raises(Exception) as exc_info:
            result = ch._hex_wrapper(values)
    else:
        result = ch._hex_wrapper(values)
        assert set(result) == set(exp)


@pytest.mark.parametrize(
    "reason, pgn, rgb, fade_function,raise_error",
    [
        ("evenly", "1. d4", "#fff", "evenly", False),
        ("last2", "1. d4", "#fff", "last2", False),
        ("rgb without #", "1. d4", "fff", "evenly", True),
        ("invalid rgb", "1. d4", "invalidrgb", "evenly", True),
        # ("TODO invalid pgn","invalid pgn", "#fff", "evenly", True),
        ("invalid function", "1. d4", "#fff", "invalid_function", True),
    ],
)
def test_print_history(reason: str, pgn: str, rgb: str, fade_function: str, raise_error: bool, tmp_dir: Path) -> None:
    ch = ChessboardHistory()

    if raise_error:
        with pytest.raises(ValueError) as exc_info:
            ch.print_history(pgn=pgn, rgb=rgb, output_path=tmp_dir, fade_function=fade_function)
    else:
        ch.print_history(pgn=pgn, rgb=rgb, output_path=tmp_dir, fade_function=fade_function)


def test_print_history_output(tmp_dir: Path):
    ch = ChessboardHistory()
    pgn = "1. d4"
    rgb = "#fff"
    fade_function = "evenly"

    # valid dir
    ch.print_history(pgn=pgn, rgb=rgb, output_path=tmp_dir, fade_function=fade_function)
    exp_file = Path(tmp_dir / "chess_history.svg")
    assert exp_file.exists()

    # invalid dir
    tmp_dir = Path("this-dir-doesnt-exist")
    with pytest.raises(ValueError) as exc_info:
        ch.print_history(pgn=pgn, rgb=rgb, output_path=tmp_dir, fade_function=fade_function)


@pytest.mark.skip(reason="Test placeholder!")
def test_gen_evenly(values) -> None:
    pass


@pytest.mark.skip(reason="Test placeholder!")
def test_gen_last_n(values) -> None:
    pass
