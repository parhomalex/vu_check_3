from threading import Thread

# Клас дозволяє створювати потоки, які можуть приймати аргументи та повертати значення
class MyThread(Thread):
    def __init__(self, target, **kwargs):
        super().__init__(target=target, kwargs=kwargs)
        self._result = None

    def run(self):
        self._result = self._target(**self._kwargs)

    @property
    def result(self):
        return self._result
# приклад використання
# def fun_1(n, x):
#     for _ in range(n):
#         sleep(1)
#         print(f'**** {_} **** - fn1')
#     return n+x
#
# def fun_2(n, x):
#     for _ in range(n):
#         sleep(1)
#         print(f'**** {_} **** - fn2')
#     return n*x
#
# start = time()
# th1 = MyThread(target=fun_1, n=5, x=2)
# th2 = MyThread(target=fun_2, n=3, x=4)
#
# th1.start()
# th2.start()
# th1.join()
# th2.join()
# r1 = th1.result
# r2 = th2.result
# print(time()-start)
#
# print(r1,r2)