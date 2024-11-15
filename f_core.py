import os

from vus_db import vus_read_vu_tmp
from screen_search import *
from time import sleep
import keyboard as ky
import pyautogui as pui
import pytesseract
import re
from os import path
import csv
from myThread import MyThread

os_name = os.name


def find_coords(template: list | str, sec:int=1, prec:float = 0.8, my_os:str = os_name, interval:int | float = 1, pause:int | bool=False):
    """
    Function finds template on screen. For the finding it can get string with path or list of strings.
    returns tuple with coordinates or False if template wasn't found.
    :param sec: int - number of find attempts
    :param template: string or list of string with paths to templates
    :param prec: float
    :param my_os: 'posix' if MacOs or 'Other'
    :return: tuple or False
    """
    if not isinstance(template, list):
        template = [template]

    for _path in template:
        if not path.isfile(_path):
            raise Exception(f'find_coords: {_path} doesen\'t exist!')
    if pause:
        sleep(pause)
    attepmt = 0
    while attepmt < sec:
        for _tmp in template:
            x, y = Search(_tmp, prec).imagesearch()
            if x != -1:
                if my_os == 'posix':
                    return [x / 2, y / 2]
                else:
                    return [x, y]
            else:
                attepmt += 1
        sleep(interval)
    return False



def find_move(sec:int, template:str|list, plusX:int=0, plusY:int=0, click=False, pause=0, duration=0.2, prec=0.8, my_os=os_name, move_rel:bool|int = False):
    """
    Function find template on screen, move to it and click it
    :param sec: number of find attempts
    :param template: string or list of string with paths to templates
    :param plusX:
    :param plusY:
    :param click: 1 - one simple click, 2 - double click, False = no click
    :param pause: If the pause is necessary before starting of function execution
    :param duration: mouse moving duration to template on screen
    :param prec:
    :param my_os: 'posix' if MacOs or 'Other'
    :param move_rel: int param add if active param click. Move away mouse after click
    :return:
    """
    sleep(pause)
    coord = find_coords(sec=sec, template=template, prec=prec, my_os=my_os)
    if coord:
        x = coord[0] + plusX
        y = coord[1] + plusY
        pui.moveTo(x=x, y=y, duration=duration)
        if click == 1:
            pui.click()
        if click == 2:
            pui.doubleClick()
        if move_rel:
            pui.moveTo(x+move_rel, y+move_rel)
        return True
    else:
        return False


def type_string(string: str | int | float, my_os = os_name):
    """
    Function gets string and types it.
    if string is empty returns False.
    Returns True.
    """
    if isinstance(string, int | float):
        string = str(string)
    if string == '':
        return False
    if my_os == 'posix':
        for symbol in string:
            pui.write(symbol)
        return True
    else:
        for symbol in string:
            ky.write(symbol)
        return True

def press_key(key, my_os = os_name):
    """
    Function get the key name as string and press it
    :param key: string
    :param my_os: 'posix' if MacOs or 'Other'
    :return: bool
    """
    if my_os == 'posix':
        pui.press(key)
    else:
        ky.press_and_release(key)

def sample_name(sec: int, dict_tmp: dict, prec: float = 0.8):
    """
    This function gets number of attempts in variable sec, dictionary where key is
    the path to sample and precision (in default is 0.8).
    Function is looking for sample on screen. If sample was found, returns sample.
    Else returns False.
    """
    if not isinstance(dict_tmp, dict):
        return False
    attempt = 0
    while True:
        if attempt == sec:
            return False
        sleep(1)
        for sample, path in dict_tmp.items():
            result = Search(path, prec).imagesearch()
            if result[0] > -1:
                return sample
        attempt += 1

def screenshot_template(template, sec=10, plusX=0, plusY=0, h=50, w=50, filePath=None, my_os = os_name):

    """
    function finds template on screen and makes a screenshot if template was found.
    :param template: path to template
    :param sec: number of attempts
    :param plusX: correction x coord
    :param plusY: correction Y coord
    :param h:
    :param w:
    :param filePath: path to file if it is needs to save. in default is none
    :param my_os: posix | else
    :return: False | image
    """
    coords = find_coords(sec=sec, template=template)
    if coords:
        if my_os == 'posix':
            x = coords[0]*2 + plusX
            y = coords[1]*2 + plusY
        else:
            x = coords[0] + plusX
            y = coords[1] + plusY
    else:
        return False
    return pui.screenshot(imageFilename=filePath, region=(x,y,w,h))


def find_multiple(template:list|str, sec=15):
    """
    The function is looking for a few samples asynchronous from the list.
    Returns a list that contains coordinates of each sample or False in not found on screen
    :param template: path to template
    :param sec: number of attempts
    :return: list
    """
    my_list = [MyThread(target=find_coords, sec=sec, template=path) for path in template]
    for th in my_list:
        th.start()
    for th in my_list:
        th.join()
    return [th.result for th in my_list]

def find_multiple_names(template:list|str, sec:int=15, prec:float=0.85):
    names = [path.split(sep='/')[-1].split(sep='.')[0] for path in template]
    my_list = [MyThread(target=find_coords, sec=sec, template=path, prec=prec) for path in template]
    for th in my_list:
        th.start()
    for th in my_list:
        th.join()
    result = [th.result for th in my_list]

    #return {k: bool(v) for k, v in zip(names, result)}
    return [k for k, v in zip(names, result) if v]



def is_not_on_screen(template:str|list, sec:int=5, prec:float=0.8, pause:int=0):
    """
    The function returns True when sample disappears from the screen if after performing the function remained on the screen, returns False.
    :param template: path to template
    :param sec: number of attempts
    :param prec:
    :param pause:
    :return:
    """
    if pause > 0:
        sleep(pause)
    n = 0
    while n != sec:
        if not find_coords(sec=1, template=template, prec=prec):
            return True
        n += 1
        sleep(1)
    return False

def scrolling_page(count_scrolls:int = 10, length_scroll:int = 5, pause:float = 0.2):
    n = 0
    while n < count_scrolls:
        shot1 = pui.screenshot()
        for _ in range(length_scroll):
            pui.scroll(-5)
        n+=1
        shot2 = pui.screenshot()
        if shot1 == shot2:
            return False
        sleep(pause)
    return True


def check_is_element(template:str, element_name:str, csv_file_name:str):
    vu_credentials = vus_read_vu_tmp('tmp/vu_credentials_tmp.csv')
    exist_on_page = False
    if find_coords(template=template, sec=1):
        exist_on_page = True

    row_for_write = [vu_credentials[0], element_name, exist_on_page]

    with open(csv_file_name, 'a') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(row_for_write)
        f_object.close()
