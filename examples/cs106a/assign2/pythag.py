import math

from spgl.util.simpio import get_positive_real

def compute_hypotenuse(a, b):
    return math.hypot(a, b)

if __name__ == '__main__':
    print("Enter values to compute the Pythagorean theorem.")
    a = get_positive_real('a:')
    b = get_positive_real('a:')
    print('c = {}'.format(compute_hypotenuse(a, b)))
