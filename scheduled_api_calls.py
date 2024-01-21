# Import libraries
import threading
import sched
from loguru import logger
import requests
from datetime import datetime
import multiprocessing as mp
import time


URL = "https://jsonplaceholder.typicode.com/todos/1"
INTERVAL = 0.1
MAX_NR_THREADS = 100
MAX_NR_TASKS = 500

class Threading():
    def __init__(self, sub_queue):
        self.threads_to_join = []
        self.sub_queue = sub_queue
        self.list_of_results = []
    
    def start_threads(self):
        if not self.sub_queue.empty():
            url = self.sub_queue.get(block=True, timeout=1)
            thread = threading.Thread(target = self.work_on_requests, args = (url,))
            logger.info(f"{thread} working on request...")
            thread.start()
            self.threads_to_join += thread,
        else:
            pass
    
    def work_on_requests(self, url):
        #response = requests.get(url = URL).status_code#.json()
        #self.list_of_results += response,
        time.sleep(5)
        self.list_of_results += "True",
    
    def work_through_queue(self):
        sc = sched.scheduler()
        while not self.sub_queue.empty():
            sc.enter(INTERVAL, 1, self.start_threads)#, (self.sub_queue,))
            sc.run()
    
    def close_threads(self):
        for i in self.threads_to_join:
            i.join()
    
    def get_results(self):
        return self.list_of_results


class Create_Queue():
    def __init__(self, number_of_tasks):
        self.number_of_tasks = number_of_tasks
        self.m = mp.Manager()
        self.queue = self.m.Queue()
    
    def fill_queue(self):
        for i in range(0, self.number_of_tasks):
            self.queue.put(URL)
    
    def get_queue(self):
        return self.queue


class Work_through_Queue():

    def __init__(self):
        queue_gen = Create_Queue(MAX_NR_TASKS)
        queue_gen.fill_queue()
        self.queue_filled = queue_gen.get_queue()
        self.result_list = []
    
    def work_through_subqueues(self):
        
        while not self.queue_filled.empty():

            sub_queue = mp.Manager().Queue()

            for i in range(0, MAX_NR_THREADS):
                #if not self.queue.empty():
                sub_queue.put(self.queue_filled.get(block=True, timeout=3))
                #else:
                #    pass
            
            parted_work = Threading(sub_queue = sub_queue)
            parted_work.work_through_queue()
            parted_work.close_threads()
            filled_result_list = parted_work.get_results()

            for i in filled_result_list:
                self.result_list += i,

            logger.info("A part of the queue was done...")
        
    def collect_results(self):
        return self.result_list


    
def run():
    working = Work_through_Queue()
    working.work_through_subqueues()
    results = working.collect_results()
    print(f"First result: {results[0]}")



if __name__ == "__main__":
    starttime = datetime.now()
    run()
    logger.success(f"Done. Took {datetime.now() - starttime}")