import random
import re

def check_dice_input(input):



def parse_roll_string(roll):
    roll_expr = roll[0]
    roll_str = roll[1]
    # Is this a pool or regular roll?
    if any(char in roll_expr for char in "<>="):
        # pool stuff
        expr_match = re.match(r'(\d*)d(\d+)([<>=])(\d+)', roll_expr)
        die_c = int(expr_match.group(1)) if expr_match.group(1) else 1
        die_s = int(expr_match.group(2))
        tar_type = expr_match.group(3)
        tn = int(expr_match.group(3))

        if die_c == 0:
            raise ValueError("Number of dice cannot be 0.")
        if die_s == 0:
            raise ValueError("Die size cannot be 0.")

        rolls = roll_dice(die_c, die_s)

        pool_dict = pool_roll(rolls, tar_type, tn)

        return pool_dict

    else:
        return None
    # non pool stuff


def roll_dice(count, size):
    rolls_out = []
    rolls_out.extend(random.randint(1, size) * count)
    return rolls_out

def pool_roll(rolls, tar_type, tn):
    succ_count = 0
    rolls_pretty = rolls

    if tar_type == '>':
        for i in range(len(rolls)):
            if rolls[i] >= tn:
                succ_count += 1
                rolls_pretty[i] = str(f'**{rolls_pretty[i]}**')
    elif tar_type == '<':
        for i in range(len(rolls)):
            if rolls[i] <= tn:
                succ_count += 1
                rolls_pretty[i] = str(f'**{rolls_pretty[i]}**')
    elif tar_type == '=':
        for i in range(len(rolls)):
            if rolls[i] == tn:
                succ_count += 1
                rolls_pretty[i] = str(f'**{rolls_pretty[i]}**')

    pool_dict = {
        "rolls_int": rolls,
        "rolls_str": rolls_pretty,
        "succ": succ_count
    }

    return pool_dict