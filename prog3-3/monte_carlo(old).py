import os
import math

RUNS = 250_000_000
# RUNS = 800000
ACCURACY = 16


class MonteCarlo:
    counter_inside = 0
    counter_outside = 0
    was_inside = False

    def pow(self, base=2, exp=8):
        if exp == 0:
            return_value = 1
        elif exp == 1:
            return_value = base
        else:
            return_value = pow(base, exp % 2) \
                           * pow(base, exp / 2) \
                           * pow(base, exp / 2)
        return return_value

    def sqrt(self, root):
        x_factor = root
        y_factor = (x_factor + 1) // 2
        while y_factor < x_factor:
            x_factor = y_factor
            y_factor = (x_factor + root // x_factor) // 2
        return x_factor

    def getRandomNumber(self):
        bytes_x = os.getrandom((int)(ACCURACY / 8))
        int_x = int.from_bytes(bytes_x, byteorder='big')
        return int_x

    def monte_carlo(self):
        for i in range(0, RUNS):
            int_x = self.getRandomNumber()
            int_y = self.getRandomNumber()

            length = self.sqrt(pow(int_x, 2) + pow(int_y, 2))
            # print(length)

            if length / pow(2, ACCURACY) < 1:
                self.counter_inside = self.counter_inside + 1
                self.was_inside = True
            else:
                self.counter_outside = self.counter_outside + 1
                self.was_inside = False

            if i > 1 and (i % 7500 == 0):
                print("Runs {:,}: ".format(i))
                print("Pi now: ", self.counter_inside
                      / (self.counter_inside + self.counter_outside) * 4)
                # print('{}  RandomNumber: {}'.format(self.was_inside, length / pow(2, ACCURACY)))

        print("Pi: ", self.counter_inside / (self.counter_inside + self.counter_outside) * 4)


def main():
    monte_carlo = MonteCarlo()
    monte_carlo.monte_carlo()


if __name__ == "__main__":
    main()
