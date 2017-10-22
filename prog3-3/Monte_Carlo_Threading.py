import os
import math
import threading

RUNS = 2_500_000
THREADS = 2
CYCLE = (int)(RUNS / THREADS)
ACCURACY = 256


class MonteCarloData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.counter_inside = 0
        self.counter_outside = 0

    def run(self):
        pass


class MonteCarlo(threading.Thread):
    lock = threading.Lock()

    def __init__(self, monte_carlo_data, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.monte_carlo_data = monte_carlo_data
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.counter_inside = 0
        self.counter_outside = 0

    @staticmethod
    def pow(base=2, exp=8):
        if exp == 0:
            return_value = 1
        elif exp == 1:
            return_value = base
        else:
            return_value = pow(base, exp % 2) \
                           * pow(base, exp / 2) \
                           * pow(base, exp / 2)
        return return_value

    @staticmethod
    def sqrt(root):
        x_factor = root
        y_factor = (x_factor + 1) // 2
        while y_factor < x_factor:
            x_factor = y_factor
            y_factor = (x_factor + root // x_factor) // 2
        return x_factor

    @staticmethod
    def getRandomNumber():
        bytes = os.getrandom((int)(ACCURACY / 8))
        integer = int.from_bytes(bytes, byteorder='big')
        return integer

    def run(self):
        for i in range(1, CYCLE):
            self.iteration()
            #self.iterationMath()
            if i % 7500 == 0:
                #MonteCarlo.lock.acquire()
                self.updateData(i)
                #MonteCarlo.lock.release()
        self.updateData(CYCLE)

    def iteration(self):
        int_x = self.getRandomNumber()
        int_y = self.getRandomNumber()

        length = self.sqrt(pow(int_x, 2) + self.pow(int_y, 2))

        if length / self.pow(2, ACCURACY) < 1:
            self.counter_inside = self.counter_inside + 1
        else:
            self.counter_outside = self.counter_outside + 1

    def iterationMath(self):
        int_x = self.getRandomNumber()
        int_y = self.getRandomNumber()

        length = math.sqrt(pow(int_x, 2) + math.pow(int_y, 2))

        if length / math.pow(2, ACCURACY) < 1:
            self.counter_inside = self.counter_inside + 1
        else:
            self.counter_outside = self.counter_outside + 1

    def updateData(self, run):
        self.monte_carlo_data.counter_inside += self.counter_inside
        self.monte_carlo_data.counter_outside += self.counter_outside

        self.output(run)

        self.counter_inside = 0
        self.counter_outside = 0

    def output(self, run):
        if self.counter_outside != 0:
            print("{} Runs: {} Pi now: {}"
                  .format(self.thread_name, run, self.counter_inside
                          / (self.counter_inside + self.counter_outside) * 4))
            print("Global Pi with {} Values: {}".format(
                self.monte_carlo_data.counter_inside
                + self.monte_carlo_data.counter_outside
                , self.monte_carlo_data.counter_inside
                / (self.monte_carlo_data.counter_inside +
                   self.monte_carlo_data.counter_outside) * 4))


def main():
    threads = []
    montecarlodata = MonteCarloData()

    for i in range(0, THREADS):
        thread = MonteCarlo(montecarlodata, i, "Thread {}".format(i))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    print("Exiting Main Thread")

    print("Finished Pi with {} Values: {}".format(
        montecarlodata.counter_inside
        + montecarlodata.counter_outside
        , montecarlodata.counter_inside
        / (montecarlodata.counter_inside +
           montecarlodata.counter_outside) * 4))


if __name__ == "__main__":
    main()
