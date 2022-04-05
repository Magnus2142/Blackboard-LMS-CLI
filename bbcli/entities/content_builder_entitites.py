from dataclasses import dataclass
from datetime import date, datetime


"""
OPTIONS DATA CLASSES
"""


@dataclass
class DateInterval:
    start_date: date = None
    end_date: date = None


@dataclass
class StandardOptions:
    hide_content: bool = False
    reviewable: bool = False
    date_interval: DateInterval = DateInterval()


@dataclass
class FileOptions:
    launch_in_new_window: bool = False


@dataclass
class WeblinkOptions:
    launch_in_new_window: bool = False


@dataclass
class GradingOptions:
    due: datetime = None
    attempts_allowed: int = 0
    grade_schema_id: str = ''
    is_unlimited_attemps_allowed: bool = True
    score_possible: int = 0


"""
CONTENT-TYPE DATA CLASSES
"""


@dataclass
class FileContent:
    upload_id: str
    file_name: str
    mime_type: str
    # Options are Rename, Replace, ThrowError
    duplicate_file_handling: str = 'Rename'
