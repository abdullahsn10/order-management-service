#!/bin/bash

# This script is used to start the application migrations
alembic upgrade head

# Start the application
python server.py



