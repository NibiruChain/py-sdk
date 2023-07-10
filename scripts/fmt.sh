#!/bin/bash
poetry run black .
poetry run isort .
flake8 pysdk
flake8 tests
flake8 examples
