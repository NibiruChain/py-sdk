#!/bin/bash
poetry run black .
poetry run isort .
flake8 nibiru
flake8 tests
flake8 examples
