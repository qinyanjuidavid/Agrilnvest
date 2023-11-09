#!/bin/bash

# Define the path to your virtual environment
VENV_PATH="/venv"

# Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    python3.9-m venv "$VENV_PATH"
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Create the "static" folder if it doesn't exist
STATIC_DIR="/modules/static"
if [ ! -d "$STATIC_DIR" ]; then
    mkdir -p "$STATIC_DIR"
fi

# Install requirements
pip install -r requirements/production.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

# Run collectstatic without prompting
python3.9 manage.py collectstatic --noinput
