import tmp_path
from f_core import find_coords, find_move, type_string, is_not_on_screen, screenshot_template
import pytesseract
import re

def vum_is_on_screen(count_attempt = 3, sec = 1):
    """
    Function is looking for VUM on screen
    :return: True|False
    """
    if find_coords(template=tmp_path.vum_logo, sec=sec):
        return True
    else:
        attempt = 0
        while True:
            if attempt == count_attempt:
                print('vum_is_on_screen: VUM wasn\'t found on screen after 3 attempts!')
                return False
            if find_move(template=tmp_path.vum_panel_icon,sec=1,pause=1,click=1,plusX=15,plusY=15):
                if find_coords(template=tmp_path.vum_logo, sec=2):
                    return True
                else:
                    attempt += 1
            else:
                print('vum_is_on_screen: VUM panel icon wasn\'t found!')
                return False

def vum_login_vu(id:str|int):
    """
    Function login VU.
    Inserts the VU id to VUM search row ckicks the Find by id button and clicks Login button
    :param id: Virtual User id
    :return: True or False
    """
    if not vum_is_on_screen():
        raise Exception("vum_login_vu: VUM was\'t found on screen!")

    if not find_move(sec=3, template=tmp_path.vum_logo, plusX=175, plusY=70, click=2, move_rel=100):
        print("vum_login_vu: VUM logo was\'t found on screen!")
        return False

    type_string(string=id)

    if not find_move(sec=3, template=tmp_path.vum_logo, plusX=300, plusY=90, click=1, move_rel=100):
        print("vum_login_vu: VUM logo was\'t found on screen!")
        return False

    if not find_move(sec=3, template=tmp_path.vum_logo, plusX=50, plusY=120, click=1, move_rel=100):
        print("vum_login_vu: VUM logo was\'t found on screen!")
        return False

    if is_not_on_screen(template=tmp_path.vum_logo, sec=3):
        return True
    else:
        return False

def vum_logout_vu(count_attempt = 3):
    """
    Function Logout VU.
    :param count_attempt:
    :return:
    """
    if not vum_is_on_screen():
        raise Exception("vum_logout_vu: VUM was\'t found on screen!")

    attempt = 0
    while True:
        if attempt == count_attempt:
            print("vum_logout_vu: Logout VU if filed after 3 attempts!")
            return False
        if not find_move(sec=3, template=tmp_path.vum_logout_btn, click=1, plusX=20, plusY=25, move_rel=100):
            attempt += 1
        return True

def vum_save_coockies(count_attempt:int=3, sec:int=5):
    if not vum_is_on_screen():
        raise Exception("vum_save_coockies: VUM was\'t found on screen!")

    attempt = 0
    while True:
        if attempt == count_attempt:
            print(f"vum_save_coockies: Button Ok was\'t found after {attempt} attempts!")
            return False
        # move to save cookies btn
        if not find_move(sec, template=tmp_path.vum_logo, plusX=50, plusY=375, click=1, move_rel=50):
            print(f"vum_save_coockies: Button Save coockies wasn\'t pushed!")
            return False
        # move to ok btn
        if find_move(sec, template=tmp_path.vum_ok_btn, click=1, plusX=20, plusY=15):
            if is_not_on_screen(sec=5, template=tmp_path.vum_ok_btn):
                return True
        attempt += 1

def vum_unlock_vu(count_attempt:int=3, sec:int=5):
    if not vum_is_on_screen():
        raise Exception("vum_unlock_vu: VUM was\'t found on screen!")

    attempt = 0
    while True:
        if attempt == count_attempt:
            print(f"vum_unlock_vu: Button Ok was\'t found after {attempt} attempts!")
            return False
        # move to unlock btn
        if not find_move(sec, template=tmp_path.vum_logo, plusX=50, plusY=430, click=1, move_rel=-50):
            print(f"vum_unlock_vu: Button Unlock virtual wasn\'t pushed!")
            return False
        # move to ok btn
        if find_move(sec, template=tmp_path.vum_ok_btn, click=1, plusX=20, plusY=15):
            if is_not_on_screen(sec=5, template=tmp_path.vum_ok_btn):
                return True
        attempt += 1

def vum_get_vu_start_status(sec:int = 10):
    if not vum_is_on_screen():
        print(f"vum_get_vu_start_status: VUM was\'t found on screen!")
        return False

    img = screenshot_template(sec=sec, template=tmp_path.vum_logo, plusX=210, plusY=215, h=25, w=450)
    string = pytesseract.pytesseract.image_to_string(img)
    try:
        result = re.search('True', string).group()
    except:
        result = re.search('False', string).group()
    return result

