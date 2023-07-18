#!/bin/bash
poetry run black src/chessboard_history/
poetry run isort
poetry run bandit -r src/chessboard_history
poetry run safety check
poetry run mypy src/chessboard_history