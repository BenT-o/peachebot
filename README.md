# peachebot
Welcome to peachebot. A discord bot project by ben.

## Commands
### !hello
peachebot will respond, good way to make sure he's online and listening.

### !svmode
Switches between ON and OFF. When ON d6 rolls are not totalled and instead displayed in a sorted array. Defasult OFF.

### !roll
Roll functionality. Takes either standard rolls (!roll 2d6+4) or pool rolls with a target number (!roll 6d10>5).
No other text can suffix the roll currently.

For regular rolls multiple dice and mods can be included as both positives or negatives in any order except using a
negative at the start of the roll (e.g. !roll -2d6+4 - which should instead be input as !roll 4-2d6).

For pool rolls either > or < can be used to indicate higher or lower than the target respectively. Successes are counted
inclusive of the target number.