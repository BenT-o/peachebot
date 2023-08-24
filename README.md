# peachebot
Welcome to peachebot. A discord bot project by ben.

## Commands
### !hello
peachebot will respond, good way to make sure he's online and listening.

### !svmode
Switches between ON and OFF. When ON d6 rolls are not totalled and instead displayed in a sorted array. Default OFF.

### !roll
Roll functionality. Takes either standard rolls (!roll 2d6+4) or pool rolls with a target number (!roll 6d10>5).\
Text can be added after the rolls to help specify what you're rolling.

For non-pool rolls you can suffix each die definition with kh/kl/dh/dl to keep/droll highest/lowest dice from the roll.\
For example, !roll 2d20kh1+4 will roll 2d20s but only keep the highest as if rolling with advantage.

For regular rolls multiple dice and mods can be included as both positives or negatives in any order except using a
negative at the start of the roll (e.g. !roll -2d6+4 - which should instead be input as !roll 4-2d6).

Maximum rolls on dice will be underlined, with natural 20s celebrated.

For pool rolls either > or < can be used to indicate higher or lower than (and equal to) the target respectively. 
Successes are counted inclusive of the target number. Rolls meeting the target number will be in bold.

### !stats
Displays stats for rolls made in the current session of the bot. Peache will print out a message per user detailing 
the following info:\
    - Total number of dice rolled\
    - Average percentile rolled on dice\
        (Dice percentile shows how high you rolled relative to the size of the dice, i.e. 80 on d100 is same percentile
        as 16 on a d20)\
    - Best roll on a die by percentile\
    - Worst roll on a die by percentile\
        (In both these cases the same percentile is valued more lucky on a higher sided die, e.g. an 80 on d100 is more
        lucky than a 16 on d20)\
    - Number of maximums rolled on die\
    - Number of minimums rolled on die\
    - Total number of d20s rolled\
    - Average rolled on d20s\
    - Best result on a d20\
    - Worst result on a d20\
    - Total number of nat 20s and nat 1s\

### !sos
Displays stats of d10 pool rolls made in the current session of the bot. Peache will print out a message per user
detailing the following info:\
    - Total number of rolls made and total number of dice rolled\
    - Averge number of dice rolled per check, average successes per check, average TN of all checks\
    - Largest pool, TN of this pool and number of successes achieved\
    - Smallest pool, TN of this pool and number of successes achieved\
        (Earlier rolls are prioritised in both cases)\
    - Luckiest roll, its successes, number of dice and luck%\
    - Unluckiest roll, its successes, number of dice and luck%\
    - Overall luck%\
        (luck% is calculated by taking % of expected successes achieved and subtracting 100, giving a proportion of
        die which met their average expected value where 0 is as expected (4 successes on 10 dice with TN7))