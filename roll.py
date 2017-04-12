from re import findall
from random import choice


def roll(text):

    all_dices = findall('\d*к\d+', text.lower())

    result_overall = []

    for dice in all_dices:
        rolls = dice.split('к')
        if rolls[0] != '':
            result = 0
            for i in range(int(rolls[0])):
                result += choice(range(int(rolls[1]))) + 1
            result = str(result)
        else:
            result = str(choice(range(int(rolls[1]))) + 1)

        result_overall.append(result)

    string = ''.join('%s = %s \n' % (all_dices[i], result_overall[i]) for i in range(len(result_overall)))

    return string

if __name__ == '__main__':

    test = ['к6', 'asdfg 2к6', '2к7 ghbdtn 2к9 фывафыва 5к7', '6к6', 'к8']

    for i in test:
        print(roll(i))
        print('\n')
