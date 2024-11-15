from status import main_menu
from checking_pull import checking_pull
print("VUs checking v3!")

while True:
    print(main_menu)
    choosen_option = input('\n=> ')
    if choosen_option == '1':
        print('Run checking!')
        checking_pull()
    elif choosen_option == '2':
        print('Run clearing checking list!')
    elif choosen_option == '3':
        print('Run test.py')
        import test
        break
    elif choosen_option == '0':
        print('Exit from program!')
        break
    else:
        print('Choose 1, 2, 3 or 0')


