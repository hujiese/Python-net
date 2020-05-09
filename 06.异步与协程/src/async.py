#!/usr/bin/python3

import threading
import asyncio

@asyncio.coroutine
def task_1():
    while True:
        print("--This is task 1!--before %s"  %(threading.currentThread()))
        yield from asyncio.sleep(1)
        print("--This is task 1!--after %s"  %(threading.currentThread()))

@asyncio.coroutine
def task_2():
    while True:
        print("--This is task 2!--before %s"  %(threading.currentThread()))
        yield from asyncio.sleep(1)
        print("--This is task 2!--after %s"  %(threading.currentThread()))

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	tasks = [task_1(), task_2()]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()