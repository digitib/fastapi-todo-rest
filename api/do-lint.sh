#!/bin/bash

set -u
set -e

echo
echo "# running black"
echo

black . --check
echo "✔️ black didn't find any issues"

echo
echo "# running isort"
echo

isort --check-only .
echo "✔️ isort didn't find any issues"

echo
echo "# running flake8"
echo

flake8
echo "✔️ flake8 didn't find any issues"

echo
echo "# running mypy"
echo

mypy .
echo "✔️ mypy didn't find any issues"

echo
echo "🟢 all checks have passed successfully"
echo