"""
Monte Carlo
"""
import time
import math
import secrets
import array
from multiprocessing import Process, Array
import numpy as np

RUNS = 2_500_000_000
THREADS = 8
CYCLE = int(RUNS / THREADS)
ACCURACY = 128
WAITING_TIME = 0.5
BORDER = math.pow(2, ACCURACY)


class MonteCarlo(Process):
    """
    Class to calculate Pi with Monte Carlo
    """

    def __init__(self, hits, thread_id, thread_name):
        """
        init of MonteCarlo
        :param hits: holds the number of hits and miss
        :param thread_id: ID of the thread
        :param thread_name: name of the thread
        """
        super(MonteCarlo, self).__init__()
        self.hits = hits
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.counter_inside = 0
        self.counter_outside = 0

    @staticmethod
    def secrets_randbits():
        """
        gets random data from secrets.randbits
        :return:
        """
        integer = secrets.randbits(ACCURACY)
        return integer

    def run(self):
        """
        starts the thread with calculation and pushing of the data
        :return:
        """
        for i in range(1, CYCLE):
            self.iteration()
            if i % 10000 == 0:
                self.update_data()
        self.update_data()

    def iteration(self):
        """
        trys to calculate py with system methods
        :return:
        """
        int_x = self.secrets_randbits()
        int_y = self.secrets_randbits()
        length = math.sqrt(int_x * int_x + int_y * int_y)

        if length / BORDER < 1:
            self.counter_inside = self.counter_inside + 1
        else:
            self.counter_outside = self.counter_outside + 1

    def update_data(self):
        """
        pushed the data of the single thread to monte_carlo_data
        :param run:
        :return:
        """
        self.hits[0] += self.counter_inside
        self.hits[1] += self.counter_outside

        self.counter_inside = 0
        self.counter_outside = 0

    def output(self, run):
        """
        prints the output with remaining run as mark of the current round
        :param run:
        :return:
        """
        if self.counter_outside != 0:
            print("{} Runs: {} Pi now: {}"
                  .format(self.thread_name, run, self.counter_inside
                          / (self.counter_inside + self.counter_outside) * 4))


class MonteCarloData(Process):
    """
    Class to hold data for Monte Carlo
    """

    def __init__(self, hits):
        """
        init for Monte Carlo Data
        """
        super(MonteCarloData, self).__init__()
        self.hits = hits

    def run(self):
        """
        prints current value of py with remaining to to completion
        :return:
        """
        last_counter = 0
        current_counter = self.hits[0] + self.hits[1]
        step_counter = array.array('i')

        while (RUNS - current_counter) > RUNS / 100:
            self.output()
            current_counter = self.hits[0] + self.hits[1]

            if len(step_counter) < 200:
                step_counter.append(current_counter - last_counter)
            else:
                step_counter = step_counter[1:]
                step_counter.append(current_counter - last_counter)

            if not step_counter:
                pass
            else:
                average_steps = np.sum(step_counter) / len(step_counter)
                remaining_time = ((RUNS - current_counter) / average_steps) * WAITING_TIME
                remaining_time_in_minutes = int((remaining_time / 60) % 60)
                remaining_time_in_hours = int(remaining_time / 60 / 60)

                print("Remaining Time: {:0.2f} seconds ({:02d}:{:02d} HH:MM) \n"
                      .format(remaining_time
                              , remaining_time_in_hours
                              , remaining_time_in_minutes))

            last_counter = self.hits[0] + self.hits[1]
            time.sleep(WAITING_TIME)

    def output(self):
        """
        prints the output with remaining run as mark of the current round
        :param run:
        :return:
        """
        print("Global Pi with {:,} Values: {:0.15f}".format(
            self.hits[0]
            + self.hits[1]
            , self.hits[0]
            / (self.hits[0] +
               self.hits[1]) * 4))


def main():
    """
    calls the main function for pylint
    :return:
    """
    threads = []
    hits = Array('i', range(2))
    montecarlodata = MonteCarloData(hits)
    montecarlodata.start()
    threads.append(montecarlodata)

    for i in range(0, THREADS):
        thread = MonteCarlo(hits, i, "Thread {}".format(i))
        thread.start()
        threads.append(thread)

    for single_thread in threads:
        single_thread.join()
    print("Exiting Main Thread")

    print("Finished Pi with {:,} Values: {}".format(
        hits[0]
        + hits[1]
        , hits[0]
        / (hits[0] +
           hits[1]) * 4))


if __name__ == "__main__":
    main()
