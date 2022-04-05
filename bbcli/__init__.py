"""Top-level package for RP To-Do."""
# rptodo/__init__.py

__app_name__ = "bbcli"
__version__ = "0.1.0"
# from .endpoints import *
# from .entities.Node import *
from .utils.utils import *
from .services import login
# from endpoints import get_user, get_course, get_assignments, get_course_contents

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}
