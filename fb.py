from f_core import find_coords, find_multiple_names, find_move, type_string, press_key
from brw import brw_run_new_tab, brw_is_page_reloaded, brw_close_active_tab
from pyautogui import screenshot
import tmp_path
import os
import pytesseract
if os.name != 'posix':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from status import Status
import re

def fb_is_logo_on_screen(sec:int = 1):
    if not find_coords(template=tmp_path.fb_logo, sec=sec):
        return False
    return True

def fb_is_top_menu(sec: int = 1):
    if len(find_multiple_names(template=tmp_path.fb_top_menu, sec=sec)) < 1:
        return False
    return True

def fb_is_side_menu(sec: int = 1):
    if len(find_multiple_names(template=tmp_path.fb_side_menu, sec=sec, prec=0.95)):
        return True
    return False

def fb_is_main_page(sec:int = 1):
    if fb_is_logo_on_screen(sec=sec) and fb_is_top_menu(sec=sec) and fb_is_side_menu(sec=sec):
        return True
    return False

def fb_get_count_friends():
    fotoX, fotoY = find_coords(template=tmp_path.fb_foto, sec=1)
    if fotoX < 0 or fotoY < 0:
        return False

    if os.name == 'posix':
        region = ((fotoX*2)+50,(fotoY*2)-70,350,50)
    else:
        region = (fotoX+30,fotoX[1]-50,150,50)
    img = screenshot(region=region)
    text = pytesseract.image_to_string(img)

    try:
        count_friends = re.search('([0-9K.]{1,4})? friends', text).group(1)
        if count_friends is None:
            count_friends = 0
            return count_friends
        return count_friends
    except AttributeError:
        count_friends = Status.OK
        return count_friends


def fb_get_vu_status():
    if fb_is_main_page():
        brw_run_new_tab('www.facebook.com/profile')
        if brw_is_page_reloaded():
            counnt_friends = fb_get_count_friends()
            brw_close_active_tab()
            return counnt_friends
        else:
            return Status.SLOW_LOAD
    else:
        return Status.UNDEFINED

def fb_get_problem_name():
    problem_names = tmp_path.brw_problems+tmp_path.fb_problems
    vu_status = find_multiple_names(template=problem_names, sec=1)
    if 'fb_login_btn' in vu_status:
        return Status.NOT_AUTHORIZATED
    else:
        return Status.UNDEFINED

def fb_login_vu(login:str, password:str):
    if not brw_run_new_tab('www.facebook.com/login'):
        return False
    brw_is_page_reloaded(sec=15)
    if not find_coords(template=tmp_path.fb_login_field, sec=1):
        return False
    find_move(template=tmp_path.fb_login_field, plusX=40, plusY=100, click=1, sec=1)
    type_string(login)
    find_move(template=tmp_path.fb_login_field, plusX=40, plusY=170, click=1, sec=1)
    type_string(password)
    press_key('enter')
    if fb_is_main_page():
        return True
    return False




def fb_check_vu(login:str, password:str):
    if fb_is_logo_on_screen():
        return fb_get_vu_status()
    else:
        problem = fb_get_problem_name()
        if problem == Status.NOT_AUTHORIZATED:
            if fb_login_vu(login=login, password=password):
                return fb_get_vu_status()
            else:
                return Status.NOT_AUTHORIZATED

        return Status.CHECKED