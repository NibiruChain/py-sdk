#!/bin/bash
poetry run black .
poetry run isort .
poetry run python -m pip install flake8
poetry run flake8 pysdk tests examples
