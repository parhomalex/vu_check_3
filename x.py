from f_core import find_coords
import tmp_path
from status import Status

def x_is_logo_on_screen(sec:int = 1):
    if not find_coords(template=tmp_path.x_logo, sec=sec):
        return False
    return True

def x_check_vu():
    if x_is_logo_on_screen():
        return Status.OK
    return Status.UNDEFINED