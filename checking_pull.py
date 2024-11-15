from vus_db import vus_get_vu, vus_save_vu_tmp, vus_read_vu_tmp, vus_write_error, vus_write_checking_result
from vum import vum_login_vu, vum_unlock_vu, vum_save_coockies, vum_logout_vu, vum_get_vu_start_status
from brw import brw_is_on_screen, brw_is_page_started, brw_is_fullscreen, brw_close_restore_pop_up, brw_close_window
from f_core import find_coords, find_move
from status import Status
import tmp_path
import datetime
from fb import fb_check_vu
from li import li_check_vu
from x import x_check_vu

vu_tmp_credentials_file = 'tmp/vu_credentials_tmp.csv'

def checking_pull():
    while True:
        # Result checking row implementation
        result_row = (7*[False])

        # Get next VU credentials
        vu_credentials = vus_get_vu()
        if not vu_credentials:
            print(f'\nchecking_pull: There are no any new VUs for checking!')
            return True

        # Save next VU credentials in file
        vus_save_vu_tmp(my_list=vu_credentials, path_to_file=vu_tmp_credentials_file)

        # Implementation of next VU credentials values
        vu_id, vu_pull, vu_login, vu_password = vu_credentials
        print(f'\nStart checking {vu_id} VU!')
        print(f'Credentials:\nPull: {vu_pull}\nLogin: {vu_login}\nPassword: {vu_password}')
        result_row[1] = vu_pull

        brw_close_window()

        if not vum_login_vu(vu_id):
            print(f'{vu_id} filed to login!')
            return False

        print(f'{vu_id} was found in VUM and loginning was started!')

        brw_is_page_started()
        if not brw_is_on_screen(sec=60):
            print(f'{vu_id} filed to login! Browser wasn\'t found on screen!')
            return False
        print(f'{vu_id} was loaded!')

        # Set checking date and time and add them to result list
        vu_checking_date = datetime.datetime.today().strftime('%Y-%m-%d')
        result_row[2] = vu_checking_date
        start_vu_checking_time = datetime.datetime.now()
        result_row[3] = start_vu_checking_time.strftime('%H:%M:%S')

        print(f'{start_vu_checking_time} start checking {vu_id}')

        brw_is_fullscreen()
        brw_close_restore_pop_up()

        print(vu_credentials, ' is cheking!')

        if vu_pull == 'sf_fb':
            result_row[0] = fb_check_vu(login=vu_login, password=vu_password)

        elif vu_pull =='sf_li':
            result_row[0] = li_check_vu()

        elif vu_pull =='sf_tw':
            result_row[0] = x_check_vu()
        else:
            result_row[0] = Status.NOT_CHECKED


        if not vum_unlock_vu():
            print(f'checking_pull: {vu_id} wasn\'t unlocked!')
            return False

        if not vum_save_coockies():
            print(f'checking_pull: {vu_id} coockies wasn\'t save!')
            return False

        if not vum_logout_vu():
            print(f'checking_pull: {vu_id} waan\'t logout!')
            return False

        result_row[6] = vum_get_vu_start_status()

        end_vu_checking_time = datetime.datetime.now()
        result_row[4] = end_vu_checking_time.strftime('%H:%M:%S')
        vu_checking_duration = (end_vu_checking_time - start_vu_checking_time).seconds
        result_row[5] = vu_checking_duration
        print(result_row)
        if not vus_write_checking_result(id=vu_id, list=result_row):
            print(f'checking_pull: {vu_id} checking result wasn\'t write to the checking list!')
            return False
        print(f'{end_vu_checking_time} - {vu_id} is checked!')
        print(f'Checking duration - {vu_checking_duration}')
        result_row.clear()

def catch_error(stop_event):
    print('Catch error start')
    while not stop_event.is_set():
        if find_coords(sec=2, template=tmp_path.brw_red_cross):
            find_move(sec=2, template=tmp_path.brw_continue_button, plusX=30, plusY=15, duration=0, click=1)
            vu = vus_read_vu_tmp('tmp/vu_data_tmp.csv')
            vu_id = vu[0]
            vu_pull = vu[1]
            vus_write_error(id=vu_id, pull=vu_pull)
    print('Catch error stop')



