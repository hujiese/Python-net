#!/usr/bin/python3
import time

def task_1():
    while True:
        print("--This is task 1!--before")
        yield
        print("--This is task 1!--after")
        time.sleep(0.5)

def task_2():
    while True:
        print("--This is task 2!--before")
        yield
        print("--This is task 2!--after")
        time.sleep(0.5)
        
if __name__ == "__main__":
    t1 = task_1()  # 生成器对象
    t2 = task_2()
    # print(t1, t2)
    while True:
        next(t1)  # 1、唤醒生成器t1，执行到yield后，保存上下文，挂起任务；下次再次唤醒之后，从yield继续往下执行
        print("\nThe main thread!\n")  # 2、继续往下执行
        next(t2)  # 3、唤醒生成器t2，....