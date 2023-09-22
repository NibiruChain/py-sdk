#!/bin/bash
poetry run black .
poetry run isort .
poetry run flake8
