from multiprocessing import Process, Value, Array
from func import stock

def f(a):
    #n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    #num = Value('d', 0.0)
    arr = Array('i', stock)

    p = Process(target=f, args=(arr,))
    p.start()
    p.join()

    #print(num.value)
    print(arr[:])