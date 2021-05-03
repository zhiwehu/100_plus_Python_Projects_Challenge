import time
import random


def get_divisor(n):
    '''
    Get a random divisor of n.
    :param n: The number
    :return: a divisor of n
    '''
    l = []
    for i in range(1, n + 1):
        if n % i == 0:
            l.append(i)
    return random.choice(l)


if __name__ == '__main__':
    ops = ['+', '-', '*', '/']
    start_time = time.time()
    total = 0
    correct = 0
    questions = []
    # while seconds is less than 60
    while time.time() - start_time <= 60:
        a = random.randint(1, 99)
        op = random.choice(ops)
        if op == '/':
            # if op is '/' then b is a divisor of a
            b = get_divisor(a)
        else:
            b = random.randint(1, 99)
        # Get the correct answer
        a_op_b = '{}{}{}'.format(a, op, b)
        c = int(eval(a_op_b))

        # Let user input answer
        try:
            ans = int(input('{} = '.format(a_op_b)))
        except:
            ans = ''

        # To check if correct or not
        if time.time() - start_time <= 60:
            if c == ans:
                print('Correct! Time remain {} seconds.'.format(int(60 - (time.time() - start_time))))
                correct = correct + 1
            else:
                print('Wrong answer! Time remain {} seconds.'.format(int(60 - (time.time() - start_time))))
            total = total + 1
            questions.append('{}={}'.format(a_op_b, ans))

    print('{} questions and your correct rate is {:.2f}%'.format(total, correct / total * 100))
    for q in questions:
        print(q)
