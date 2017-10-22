import os
import time
import math
import secrets
import numpy as np
import array
from multiprocessing import Process, Array

RUNS = 2_500_000_000
THREADS = 4
CYCLE = int(RUNS / THREADS)
ACCURACY = 128
WAITING_TIME = 0.5
BORDER = math.pow(2, ACCURACY)


class MonteCarlo(Process):
    def __init__(self, hits, thread_id, thread_name):
        super(MonteCarlo, self).__init__()
        self.hits = hits
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.counter_inside = 0
        self.counter_outside = 0

    @staticmethod
    def getRandomNumber():
        return MonteCarlo.getRandomNumberSystemRandom()

    @staticmethod
    def getRandomNumberSystemRandom():
        integer = secrets.randbits(ACCURACY)
        return integer

    @staticmethod
    def getRandomNumgerOsRandom():
        bytes = os.getrandom(int(ACCURACY / 8))
        integer = int.from_bytes(bytes, byteorder='big')
        return integer

    def run(self):
        for i in range(1, CYCLE):
            self.iteration()
            if i % 10000 == 0:
                self.updateData()
        self.updateData()

    def iteration(self):
        int_x = self.getRandomNumber()
        int_y = self.getRandomNumber()
        length = math.sqrt(int_x * int_x + int_y * int_y)

        if length / BORDER < 1:
            self.counter_inside = self.counter_inside + 1
        else:
            self.counter_outside = self.counter_outside + 1

    def updateData(self):
        self.hits[0] += self.counter_inside
        self.hits[1] += self.counter_outside

        self.counter_inside = 0
        self.counter_outside = 0

    def output(self, run):
        if self.counter_outside != 0:
            print("{} Runs: {} Pi now: {}"
                  .format(self.thread_name, run, self.counter_inside
                          / (self.counter_inside + self.counter_outside) * 4))


class MonteCarloData(Process):
    def __init__(self, hits):
        super(MonteCarloData, self).__init__()
        self.hits = hits

    def run(self):
        last_counter = 0
        current_counter = self.hits[0] + self.hits[1]
        step_counter = array.array('i')

        while (RUNS - current_counter) > RUNS / 100:
            self.output()
            current_counter = self.hits[0] + self.hits[1]

            if len(step_counter) < 20:
                step_counter.append(current_counter - last_counter)
            else:
                step_counter = step_counter[1:]
                step_counter.append(current_counter - last_counter)

            if len(step_counter) != 0:
                average_steps = np.sum(step_counter) / len(step_counter)
                remaining_time = ((RUNS - current_counter) / average_steps) * WAITING_TIME
                remaining_time_in_minutes = int((remaining_time / 60) % 60)
                remaining_time_in_hours = int(remaining_time / 60 / 60)

                print("Remaining Time: {:0.2f} seconds ({:02d}:{:02d} HH:MM)"
                      .format(remaining_time
                              , remaining_time_in_hours
                              , remaining_time_in_minutes))

            last_counter = self.hits[0] + self.hits[1]
            time.sleep(WAITING_TIME)

    def output(self):
        print("Global Pi with {:,} Values: {:0.15f}".format(
            self.hits[0]
            + self.hits[1]
            , self.hits[0]
            / (self.hits[0] +
               self.hits[1]) * 4))


def main():
    threads = []
    hits = Array('i', range(2))
    montecarlodata = MonteCarloData(hits)
    montecarlodata.start()
    threads.append(montecarlodata)

    for i in range(0, THREADS):
        thread = MonteCarlo(hits, i, "Thread {}".format(i))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    print("Exiting Main Thread")

    print("Finished Pi with {:,} Values: {}".format(
        hits[0]
        + hits[1]
        , hits[0]
        / (hits[0] +
           hits[1]) * 4))


if __name__ == "__main__":
    main()
