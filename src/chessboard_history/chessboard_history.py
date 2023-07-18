import io
from pathlib import Path
import numpy as np
import chess
from chess.pgn import read_game
from chess.svg import Arrow
import re
from typing import List


class ChessboardHistory:
    def __init__(self) -> None:
        pass

    def _hex_wrapper(self, input: List[int]) -> List[str]:
        """Transform a list of ints in range 0-255 to the last two digits of their hex representation."""
        l = [f"{x:#0{4}x}" for x in input]
        l = [x[-2:] for x in l]
        print(l)
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

    def print_history(self, pgn: str, rgb: str, fade_function: str = "evenly") -> None:
        """
        Args:
            pgn:
            rgb:
            fade_function: "evenly", "last2"
        """
        if fade_function not in ["evenly", "last2"]:
            raise Exception("Please provide a proper FADE_FUNCTION!")

        hex_rgb_pat = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
        if re.match(hex_rgb_pat, rgb) is None:
            raise Exception("Please provide a valid RGB value!")
        self.rgb = rgb

        pgn = io.StringIO(pgn)
        self.game = read_game(pgn)

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

        with open(Path().cwd() / "chess_history.svg", "w") as f:
            f.write(board_svg)


if __name__ == "__main__":
    pgn = "1. e4 e5 2. Qf3 Nc6 3. Bc4 Nf6 4. Ne2 Bc5 5. a3 d6 6. O-O Bg4 7. Qd3 Nh5 8. h3 Bxe2 9. Qxe2 Nf4 10. Qe1 Nd4 11. Bb3 Nxh3+ 12. Kh2 Qh4 13. g3 Nf3+ 14. Kg2 Nxe1+ 15. Rxe1 Qg4 16. d3 Bxf2 17. Rh1 Qxg3+ 18. Kf1 Bd4 19. Ke2 Qg2+ 20. Kd1 Qxh1+ 21. Kd2 Qg2+ 22. Ke1 Ng1 23. Nc3 Bxc3+ 24. bxc3 Qe2#"
    ch = ChessboardHistory()
    ch.print_history(pgn, "#ff0000", fade_function="evenly")
