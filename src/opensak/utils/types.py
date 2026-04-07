"""
src/opensak/utils/types.py — Core enumerations for file formats and cache activity.

Defines the ImportType and LogType Enums for standardized data handling.
Maps geocaching log statuses to integer values for consistent database storage.
"""

from enum import Enum, IntEnum, auto

# Import types for supported file formats
class ImportType(Enum):
    GPX = auto()
    ZIP = auto()

# Cache log types
class LogType(IntEnum):
    FOUND = 2
    DNF = 3
    NOTE = 4
    ARCHIVE = 5