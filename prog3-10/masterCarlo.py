
from __future__ import print_function

from TaskmanagerCarlo import TaskManager
import random, time

def __calculate(m, number_of_trys, number_of_parts, worker_count):
    worker_trys = number_of_trys / worker_count
    worker_trys_part = worker_trys / number_of_parts
    
    job_queue, result_queue = m.get_job_queue(), m.get_result_queue()

    in_list = []
    result_list = []    
    
    for i in range (number_of_parts * worker_count):
        random_number = int(random.random() * (2**31 -1))
        in_list.append((worker_trys_part, random_number))
    
    for parameter_set in in_list:
        job_queue.put(parameter_set)    

    job_queue.join()
    while not result_queue.empty():
        result_list.append(result_queue.get()) 
        
    print(result_list)

    hits = 0
    trys = 0

    for e in in_list:
        x = e[0]
        trys += x

    for result_tuple in result_list:
        hits += result_tuple


    print((hits)/trys * 4)


if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) != 6:
        print('usage:', argv[0], 'server_IP server_socket number_of_trys number_of_parts worker_count')
        exit(0)
    server_ip = argv[1]
    server_socket = int(argv[2])
    number_of_trys = int(argv[3])
    number_of_parts = int(argv[4])
    worker_count = int(argv[5])
    
    TaskManager.register('get_job_queue')
    TaskManager.register('get_result_queue')
    m = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
    m.connect()

    t1 = time.time()
    result = __calculate(m, number_of_trys, number_of_parts, worker_count)
    t2 = time.time()
    print(' result: ', result)
    print(' time:   ', t2-t1, ' s\n')