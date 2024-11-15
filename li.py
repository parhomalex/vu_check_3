from f_core import find_coords
import tmp_path
from status import Status

def li_is_logo_on_screen(sec:int = 1):
    if not find_coords(template=tmp_path.li_logo, sec=sec):
        return False
    return True

def li_check_vu():
    if li_is_logo_on_screen():
        return Status.OK
    return Status.UNDEFINED