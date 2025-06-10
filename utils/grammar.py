from pyparsing import (Word, nums, alphas, oneOf,
                       Optional, Combine, Group,
                       Forward, infixNotation, opAssoc,
                       ParserElement, Literal, delimitedList)

ParserElement.enablePackrat()

# --- Basic tokens ---
integer = Word(nums)
dice_count = Optional(integer, default="1")
dice_sides = integer
keepdrop = (oneOf("kh kl dh dl") + integer)
dice = Combine(dice_count + "d" + dice_sides) + Optional(keepdrop)

flatmod = Combine(Optional(oneOf("+ -")) + integer)
term = dice | flatmod

# --- Expression grammar ---
expr = Forward()
atom = (Group(dice) | flatmod)
expr <<= infixNotation(atom,
                       [
                           (oneOf('+ - < >'), 2, opAssoc.LEFT),
                       ])

# --- Multiplier and full command ---
repeat_prefix = Combine(integer + "#")
full_expression = Optional(repeat_prefix, default="1#")("count") + expr("expression")

# --- Splitting multiple expressions by commas ---
roll_command = delimitedList(Group(full_expression + Optional(Word(alphas + nums + " .'!?+-"))("comment")))


# --- Parsing !roll command ---
async def parse_roll_command(input_string):
    parsed = roll_command.parseString(input_string)

    results = []
    for item in parsed:
        count = int(item.count[:-1]) if item.count.endswith('#') else int(item.count)
        expression = item.expression
        comment = item.comment if 'comment' in item else ''
        results.append({
            "count": count,
            "expression": expression,
            "comment": comment.strip(" ,")
        })
    return results


async def build_dice(tokens):
    result = {}
    result['die_count'] = tokens['count']
    result['die_size'] = tokens['sides']
    if 'dropkeep' in tokens:
        result['keep_drop'] = {
            'type': tokens['dropkeep'],
            'num': tokens['dropkeep_num']
        }
    return{'dice': result}


async def build_number(tokens):
    return {'number': tokens[0]}
