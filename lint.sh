#!/bin/bash
poetry run black .
poetry run isort .
poetry run bandit -r src/chessboard_history
poetry run safety check
poetry run mypy src/chessboard_history
poetry run coverage run -m pytest
poetry run coverage report