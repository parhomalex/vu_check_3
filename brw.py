import tmp_path
from f_core import find_coords, find_move, type_string, press_key, is_not_on_screen, screenshot_template

def brw_is_on_screen(sec:int = 15):
    if not find_coords(template=tmp_path.brw_first_tab, sec=sec):
        return False
    return True

def brw_close_restore_pop_up(sec:int = 1):
    if not find_move(template=tmp_path.brw_restore_pop_up, plusX=300, plusY=10, sec=sec, click=2, move_rel=-50):
        return True
    attempt = 0
    while True:
        if attempt == 3:
            return False

        if find_coords(template=tmp_path.brw_restore_pop_up, sec=sec):
            find_move(template=tmp_path.brw_restore_pop_up, plusX=300, plusY=10, sec=sec, click=2, move_rel=-50)

        if is_not_on_screen(template=tmp_path.brw_restore_pop_up, sec=sec):
            attempt += 1


def brw_is_fullscreen():
    if not brw_is_on_screen():
        raise Exception("brw_is_fullscreen: Browser is not on screen!")

    if find_coords(template=tmp_path.brw_full_screen, sec=1, prec=0.95):
        return True

    if find_move(template=tmp_path.brw_small_screen,
                     sec=1,
                     click=1,
                     prec=0.95,
                     plusX=30,
                     plusY=15,
                     move_rel=100) and find_coords(
        template=tmp_path.brw_full_screen,
        sec=1,
        prec=0.95
    ):
        print('brw_is_fullscreen: Browser was turn to fullscreen!')
        return True
    return False

def brw_get_new_tab():
    if not brw_is_on_screen():
        raise Exception("brw_is_fullscreen: Browser is not on screen!")

    if not find_move(template=tmp_path.brw_new_tab, sec=1, plusX=60, plusY=15, click=1):
        print('brw_get_new_tab: New tab btn wasn\'t found')
        return False

    if find_coords(template=tmp_path.brw_google_search_row, sec=5):
        return True
    print('brw_get_new_tab: Google search row wasn\'t found')
    return False

def brw_run_new_tab(text:str):
    if not brw_get_new_tab():
        print('brw_run_new_tab: New tab wasn\'t get!')
        return False

    if not find_move(template=tmp_path.brw_addr_row_new_tab, sec=10, plusX=50, plusY=15, click=1, move_rel=50):
        print('brw_run_new_tab: New tab address row wasn\'t found!')
        return False

    type_string(text)
    press_key("enter")
    return True

def brw_close_active_tab():
    if not brw_is_on_screen():
        raise Exception("brw_is_fullscreen: Browser is not on screen!")

    if not find_move(template=tmp_path.brw_new_tab, sec=1, plusX=20, plusY=15, click=1):
        print('brw_close_active_tab: New tab btn wasn\'t found')
        return False
    return True


def brw_is_page_started(sec:int = 30):
    sec = sec*4
    if not find_coords(template=tmp_path.brw_arrows_not_loaded, sec=sec, interval=0.25):
        return True
    if not find_coords(template=tmp_path.brw_arrows_loaded, sec=sec, interval=0.25):
        return True
    find_coords(template=tmp_path.brw_arrows_not_loaded, sec=sec, interval=0.25)
    find_coords(template=tmp_path.brw_arrows_loaded, sec=sec, interval=0.25)
    return True

def brw_is_page_reloaded(sec:int = 30):
    sec = sec * 4
    find_coords(template=tmp_path.brw_arrows_loaded, sec=sec, interval=0.25)
    return True

def brw_close_window():
    if not find_move(template=tmp_path.brw_full_screen+tmp_path.brw_small_screen, sec=2, plusX=80, plusY=15, click=1):
        return True
    return False