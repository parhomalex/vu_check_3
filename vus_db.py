import datetime
import pygsheets
from random import choice
import csv
from collections import namedtuple

credentials = pygsheets.authorize(service_file='credentials/credentials.json')
sheet_id = '1wA6eIXb1IB5AamHn6O-1_KqOPE7jwu_krprUFCJGSHs'
check_list = 'check_list'
history_list = 'hist_list'
errors = 'errors'
words_list = 'words_list'
worksheet = credentials.open_by_key(sheet_id).worksheet_by_title(check_list)


def vus_get_checking_list():
    #Function reads the checking list
    """
    Function returns the checking list or False if checking list is empty
    :return: list | False
    """
    try:
        check_range = credentials.get_range(spreadsheet_id=sheet_id,
                                                 value_range=f'{check_list}!A2:H')
        if len(check_range[0][0]) == 0:
            return False
        return check_range
    except Exception as ex:
        #print(f'{Fore.LIGHTRED_EX}vus_get_check_list:{Style.RESET_ALL} {ex}')
        return False

def vus_next_vu_id():
    """
    function returns next not checked virtual user id or False if all id is checked
    or list is empty
    :return: id | False
    """
    id = False
    list = vus_get_checking_list()
    if list:
        for row in list:
            if len(row) < 1:
                print('There are empty rows in check_list')
                return False
            if len(row) == 1:
                id = row[0]
                break
    else:
        return False
    return id

def vus_get_vu():
    """
    Function gets next unchecked virtual user id from checking list and
    returns the list with vu details.
    :return: False | list [id, pull, login, password]
    """
    id = str(vus_next_vu_id())
    vu_cred = False
    #Function gets VU id and pull session and returns the tuple wich countains id, pull, login, password
    pull_range = credentials.get_range(spreadsheet_id=sheet_id, value_range=f'sf_vus!A2:D')
    #print(pull_range)
    for row in pull_range:
        if row[0] == id:
            if len(row) == 4:
                vu_cred = row
                break
            else:
                length = 4 - len(row)
                vu_cred = row + (length*[False])
    return vu_cred




def vus_write_checking_result(id, list):
    """
    Function writes checking result to checking list
    :param id: vu id
    :param list: checking result of  in 7 values
    :return False or True:
    """
    result = False
    id = str(id)
    check_range = vus_get_checking_list()
    n_row = 1
    for row in check_range:
        n_row += 1
        if row[0] == id and len(row) == 1:
            try:
                pygsheets.datarange.DataRange(start=f'B{n_row}', end=f'H{n_row}', worksheet=worksheet).update_values([list])
            except Exception as ex:
                print(f'vus_write_checking_result: {ex}')
            result = True
            break
    return result

    #Function gets the list with checking result and writes it to checking list


def vus_write_checking_history():
    """
    If all rows are filled completely in checking list, function writes them to checking history
    :return: True | False
    """
    result = False
    check_range = vus_get_checking_list()
    if not check_range:
        print('vus_write_checking_history: Chek_list is empty!')
        return result
    for row in check_range:
        if len(row) < 2:
            print('vus_write_checking_history: Chek_list is not checked compeatly!')
            return result

    history_sheet = credentials.open_by_key(sheet_id).worksheet_by_title(history_list)
    history_sheet.insert_rows(1, number=len(check_range))
    history_sheet.update_values(crange = f'A2:H{len(check_range)+1}', values=check_range)
    return True


def vus_clear_checking_list():
    """
    Function clear the checking list
    :return: True | False
    """
    attempt = 0
    credentials.open_by_key(sheet_id).worksheet_by_title(check_list).clear('A2:H')

def vus_insert_row(page_name):
    credentials.open_by_key(sheet_id).worksheet_by_title(title=page_name).insert_rows(row=1, number=1)


def vus_write_error(id, pull):
    day = datetime.datetime.today().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')
    error_data = [day, time, id, pull]
    vus_insert_row(errors)
    credentials.open_by_key(sheet_id).worksheet_by_title(title=errors).update_values(crange='A2:2', values=[error_data])

def vus_save_vu_tmp(my_list, path_to_file):
    try:
        with open(path_to_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(my_list)
    except:
        return False
    return True


def vus_read_vu_tmp(path_to_file):
    try:
        with open(path_to_file, 'r') as file:
            data = list(csv.reader(file, delimiter=','))
        return data[0]
    except:
        return False

def vus_get_word():
    try:
        words = credentials.get_range(spreadsheet_id=sheet_id, value_range=f'{words_list}!A:A')
    except:
        return 'Memes'
    if words:
        list = [el[0] for el in words]
    word = choice(list)
    if len(word) < 3:
        return 'Memes'
    return word

# class vu:
#     """
#
#     """
#     def __init__(self, session_pull):
#         self.bool = False
#         self.session_pull = session_pull
#         self.vu_credentials = self.vus_get_vu(session_pull=self.session_pull)
#         if self.vu_credentials:
#             self.bool = True
#             self.id = self.vu_credentials[0]
#             self.pull = self.vu_credentials[1]
#             self.login = self.vu_credentials[2]
#             self.password = self.vu_credentials[3]
#
#     def vus_get_vu(self, session_pull):
#         vu_cred = False
#         id = vus_next_vu_id()
#         if id:
#             id = str(id)
#         else:
#             return vu_cred
#         # Function gets VU id and pull session and returns the tuple wich countains id, pull, login, password
#         pull_range = credentials.get_range(spreadsheet_id=sheet_id, value_range=f'{session_pull}_vus!A2:D')
#         for row in pull_range:
#             if row[0] == id:
#                 if len(row) == 4:
#                     vu_cred = row
#                     break
#                 else:
#                     length = 4 - len(row)
#                     vu_cred = row + (length * [False])
#         return vu_cred



