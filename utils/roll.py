import math
import random
import re

# Takes in just the roll (3d6+2), does this one per roll string
async def rolldice(fullroll):
    # Separate rolls from mods
    rollexpr = r'(([+-]?\d*d\d+)([kd][hl]\d+)?)'
    modexpr = r'[+-]\d+(?!d\d+)'

    rollparse = re.findall(rollexpr, fullroll)
    mods = re.findall(modexpr, fullroll)
    # Convert mods to int ('+2' becomes 2, '-2' becomes -2)
    mods = [int(m) for m in mods]

    rollsdict = []
    total = 0

    for roll in rollparse:
        full = roll[0]
        die = roll[1]
        adv = roll[0]

        die_c = die.split('d')[0]
        if die_c == '':
            die_c = 1
        elif die_c == '-':
            die_c = -1
        die_s = die.split('d')[1]

        rolls = []
        if die_c < 0:
            is_neg = True
        else:
            is_neg = False
        die_c = abs(die_c)

        # Perform Rolls
        while die_c > 0:
            if is_neg:
                x = -random.randint(1, die_s)
                total = total + x
                rolls.append(x)
                #users[userid].append([x, die_s])
            else:
                x = random.randint(1, die_s)
                total = total + x
                rolls.append(x)
                #users[userid].append([x, die_s])
            die_c = die_c - 1
        print(rolls)


    # Prep logging of rolls for stats
    roller = message.author
    userlist = []
    for i in users:
        userlist.append(i[0])
    if roller in userlist:
        userid = userlist.index(roller)
    else:
        users.append([roller])
        userid = len(users) - 1

    # Prep rolled array
    for roll in roll_dice:
        splitroll = re.split(r'd', roll[0])
        c_temp = re.sub(r' *', '', splitroll[0])
        if c_temp == '' or c_temp == '+':
            die_c = 1
        elif c_temp == '-':
            die_c = 1
        elif c_temp.startswith('+'):
            die_c = int(c_temp[1:])
        else:
            die_c = int(c_temp)
        die_s = re.sub(r' *', '', splitroll[1])
        die_s = int(die_s)

        rolls = []
        if die_c < 0:
            is_neg = True
        else:
            is_neg = False
        die_c = abs(die_c)

        # Perform Rolls
        while die_c > 0:
            if is_neg:
                x = -random.randint(1, die_s)
                total = total + x
                rolls.append(x)
                users[userid].append([x, die_s])
            else:
                x = random.randint(1, die_s)
                total = total + x
                rolls.append(x)
                users[userid].append([x, die_s])
            die_c = die_c - 1
        print(rolls)

        if roll[1] == "":
            for i in range(len(rolls)):
                if rolls[i] == die_s:
                    rolls[i] = f"__{rolls[i]}__"
            else:
                rolledarray.append(str(rolls))
        else:
            advrollmod_type = roll[1][:2]
            print("advrollmod_type = " + advrollmod_type)
            advrollmod_count = int(roll[1][2:])
            print("advrollmod_count = " + str(advrollmod_count))
            sortedrolledarray = sorted(rolls)
            if advrollmod_type == 'kh':
                keep = sortedrolledarray[-advrollmod_count:]
                drop = sortedrolledarray[:-advrollmod_count]
            elif advrollmod_type == 'kl':
                keep = sortedrolledarray[:advrollmod_count]
                drop = sortedrolledarray[advrollmod_count:]
            elif advrollmod_type == 'dh':
                keep = sortedrolledarray[:-advrollmod_count]
                drop = sortedrolledarray[-advrollmod_count:]
            elif advrollmod_type == 'dl':
                keep = sortedrolledarray[advrollmod_count:]
                drop = sortedrolledarray[:advrollmod_count]
            print(drop)
            for d in drop:
                for x in rolls:
                    if x == d:
                        total = total - d
                        rolls[rolls.index(d)] = "~~" + str(rolls[rolls.index(d)]) + "~~"
                        break
            newrolls = []
            for x in rolls:
                x_int = int(re.sub(r'~', '', str(x)))
                if x_int == die_s:
                    newrolls.append(f'__{x}__')
                else:
                    newrolls.append(x)
            rolledarray.append(str(newrolls))

    mod = 0
    for x in roll_mod:
        x = re.sub(' *', '', x)
        if x.startswith('+'):
            mod = mod + int(x[1:])
        else:
            mod = mod + int(x)
    total = total + mod

    print(rolledarray)
    print('MOD: ' + str(mod))
    print('TOTAL: ' + str(total))
    print("-------")
    print(f'USER LIST = {users}')