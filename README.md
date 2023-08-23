# peachebot
Welcome to peachebot. A discord bot project by ben.

## Commands
### !hello
peachebot will respond, good way to make sure he's online and listening.

### !svmode
Switches between ON and OFF. When ON d6 rolls are not totalled and instead displayed in a sorted array. Default OFF.

### !roll
Roll functionality. Takes either standard rolls (!roll 2d6+4) or pool rolls with a target number (!roll 6d10>5).
Text can be added after the rolls to help specify what you're rolling.

For non-pool rolls you can suffix each die definition with kh/kl/dh/dl to keep/droll highest/lowest dice from the roll.
For example, !roll 2d20kh1+4 will roll 2d20s but only keep the highest as if rolling with advantage.

For regular rolls multiple dice and mods can be included as both positives or negatives in any order except using a
negative at the start of the roll (e.g. !roll -2d6+4 - which should instead be input as !roll 4-2d6).

For pool rolls either > or < can be used to indicate higher or lower than the target respectively. Successes are counted
inclusive of the target number.