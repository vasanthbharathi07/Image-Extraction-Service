#!/bin/bash

# Ensure that mypy is installed
pip install mypy

# Run mypy on the src directory (adjust the path as necessary)
mypy --ignore-missing-imports src/