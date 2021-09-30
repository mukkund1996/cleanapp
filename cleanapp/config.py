import os
from pathlib import Path

CLEANING_MASTER_SHEET = "Cleaning Master Sheet"

# Set as environment variable
CREDENTIALS_PATH = os.getenv("CREDENTIALS_JSON")

# Columns tuple
COLUMNS_ITERABLE = ("living_room", "kitchen", "bathroom_&_toilet", "trash_&_groceries")

# Persons tuple
PERSONS_TUPLE = ("mukkund", "sharanya", "giovanni", "shyam")

BG_COLORS = ["#ADD9F4", "#984447"]
