from spgl.util.simpio import get_integer

POSITIVE_INFINITY = float('inf')
NEGATIVE_INFINITY = float('-inf')

if __name__ == '__main__':
    SENTINEL = 0
    print("This program finds the largest and smallest numbers.")
    smallest, largest = POSITIVE_INFINITY, NEGATIVE_INFINITY
    while True:
        n = get_integer('?:')
        if n == SENTINEL:
            break
        if n < smallest:
            smallest = n
        if n > largest:
            largest = n
    if smallest == POSITIVE_INFINITY or largest == NEGATIVE_INFINITY:
        print('You must enter at least one value before the sentinel!')
    else:
        print('smallest:', smallest)
        print('largest:', largest)
