from re import findall
from random import choice


def throw_dice(all_dices):
    result_overall = []

    for dice in all_dices:
        rolls = dice.split('к')

        if int(rolls[0]) >= 150:
            result = 'Сам столько кидай, куропат'

        elif rolls[0] != '':
            result = 0
            for i in range(int(rolls[0])):
                result += choice(range(int(rolls[1]))) + 1
            result = str(result)
        else:
            result = str(choice(range(int(rolls[1]))) + 1)


        result_overall.append(result)

    return result_overall


def throw_dice_confirm(all_dices):
    result_overall = []

    for dice in all_dices:
        rolls = dice.split('к')
        temp = rolls[1].split('на')
        rolls[1] = temp[0]
        rolls.append(temp[1])

        if int(rolls[0]) >= 150:
            result = 'Сам столько кидай, куропат'

        elif rolls[0] != '':
            result = 0
            for i in range(int(rolls[0])):
                if choice(range(int(rolls[1]))) + 1 >= int(rolls[2]):
                    result += 1
            result = str(result)
        else:
            if choice(range(int(rolls[1]))) + 1 >= str():
                result = '1'


        result_overall.append(result)

    return result_overall


def roll(text):

    all_dices_confirm = findall('\d*к\d+на\d+', text.lower())
    for i in all_dices_confirm:
        text = text.lower().replace(i, '')

    all_dices = findall('\d*к\d+', text.lower())

    result_overall_1, result_overall_2 = [], []

    if len(all_dices) == 0 and len(all_dices_confirm) == 0:
        return u'Что то пошло не так, еще раз давай. Давай, чо ты. Еще раз какую то херню пришли, маргинал'
    if len(all_dices) != 0:
        result_overall_1 = throw_dice(all_dices)
    if len(all_dices_confirm) != 0:
        result_overall_2 = throw_dice_confirm(all_dices_confirm)

    result_overall = result_overall_1 + result_overall_2
    rolls_all = all_dices + all_dices_confirm

    string = ''.join('%s = %s \n' % (rolls_all[i], result_overall[i]) for i in range(len(result_overall)))

    return string

if __name__ == '__main__':

    test = ['к6', 'asdfg 2к6', '2к7 ghbdtn 2к9 фывафыва 5к7', '6к6', 'к8', '50к6на4']

    for i in test:
        print(roll(i))
        print('\n')
