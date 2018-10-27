from campy.util.simpio import get_integer

def hailstone(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            m = n // 2
            print('{} is even so I take half: {}'.format(n, m))
        else:
            m = 3 * n + 1
            print('{} is odd, so I make 3n + 1: {}'.format(n, m))

        n = m
        steps += 1
    return steps


if __name__ == '__main__':
    n = get_integer('Enter a number: ')
    steps = hailstone(n)
    print('The process took {} to reach 1'.format(steps))
