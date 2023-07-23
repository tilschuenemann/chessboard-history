import io
import re
from pathlib import Path
from typing import List

import chess
import numpy as np
from chess.pgn import read_game
from chess.svg import Arrow


class ChessboardHistory:
    def __init__(self) -> None:
        pass

    def _hex_wrapper(self, input: List[int]) -> List[str]:
        """Transform a list of ints in range 0-255 to the last two digits of their hex representation."""
        if any([x for x in input if x not in range(255)]):
            raise ValueError("Only ints in [0-255] supported!")

        l = [f"{x:#0{4}x}" for x in input]
        l = [x[-2:] for x in l]
        return l

    def _gen_evenly(self, len: int) -> List[str]:
        """Creates a list of two ascending hex digits from 0x01 to 0xff.

        Args:
            len: length of input to match
        """
        l = np.linspace(1, 255, len).tolist()
        l = [int(x) for x in l]
        return self._hex_wrapper(l)

    def _gen_last_n(self, len: int, n: int) -> List[str]:
        """Creates a list of two ascending hex digits: 0xc0 for the last n and 0x40 for all other.

        Args:
            len: length of input to match
            n: amount of moves with full opacity
        """
        l = [64 for _ in range(len - n)]
        l = l + [192 for _ in range(n)]
        return self._hex_wrapper(l)

    def print_history(self, pgn: str, rgb: str, output_path: Path, fade_function: str = "evenly") -> None:
        """
        Args:
            pgn:
            rgb:
            fade_function: "evenly", "last2"
        """
        if output_path.exists() is False or output_path.is_dir() is False:
            raise ValueError("Please provide a proper OUTPUT_PATH!")

        if fade_function not in ["evenly", "last2"]:
            raise ValueError("Please provide a proper FADE_FUNCTION!")

        hex_rgb_pat = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
        if re.match(hex_rgb_pat, rgb) is None:
            raise ValueError("Please provide a valid RGB value!")
        self.rgb = rgb

        self.game = read_game(io.StringIO(pgn))

        arrows = []
        board = self.game.board()
        for move in self.game.mainline_moves():
            board.push(move)
            arrow = Arrow(tail=move.from_square, head=move.to_square)
            arrows.append(arrow)

        move_count = len(arrows)
        if fade_function == "evenly":
            opacities = self._gen_evenly(move_count)
        else:
            opacities = self._gen_last_n(move_count, 2)

        for i, arrow in enumerate(arrows):
            arrow.color = f"{self.rgb}{opacities[i]}"

        board_svg = chess.svg.board(board, arrows=arrows, size=350)

        with open(Path(output_path / "chess_history.svg"), "w") as f:
            f.write(board_svg)
