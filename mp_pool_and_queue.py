from multiprocessing import Process, cpu_count, Pool, Queue
import queue
import random
from math import factorial as fc
from datetime import datetime
from dateutil.relativedelta import relativedelta
from loguru import logger
import sched
import sys

MAX_NR_TASKS = 2000
MAX_NR_RAND = 1000

def create_task():
    return random.randint(1, MAX_NR_RAND)

def calc_fc(tasks_to_calc):
    while not tasks_to_calc.empty():
        try:
            task = tasks_to_calc.get(block=True, timeout=0)
            calced_fc = fc(task)
            if "--print" in sys.argv:
                print(f"Factorial of {task} is {calced_fc}")
        except queue.Empty:
            break

def calc_fc_pool(i):
    g = fc(i)
    if "--print" in sys.argv:
        print(f"Factorial of {i} is {g}")


def run():
    
    tasks_to_calc = Queue()

    processes = []

    for i in range(0, MAX_NR_TASKS):
        tasks_to_calc.put(create_task())
    

    for w in range(cpu_count()):
        p = Process(target=calc_fc, args=(tasks_to_calc,))
        processes += p,
        p.start()
    
    for p in processes:
        p.join()


def run_pool():
    index_test = [create_task() for i in range(MAX_NR_TASKS)]
    with Pool(cpu_count()) as pool:
        pool.map(calc_fc_pool, index_test)


if __name__ == "__main__":
    start_time_queue = datetime.now()
    run()
    end_time_queue = datetime.now()
    start_time_pool = datetime.now()
    run_pool()
    end_time_pool = datetime.now()

    logger.success(f"Queue finished in {end_time_queue - start_time_queue}")
    logger.success(f"Pool finished in {end_time_pool - start_time_pool}")