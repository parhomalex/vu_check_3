from fb import fb_login_vu
from time import sleep, time

sleep(2)

t1 = time()
print(fb_login_vu('KatelynWillis923@bk.ru','cX8Kke1a9c'))
t2 = time()

print(t2 - t1)