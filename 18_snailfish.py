#############################
# --- Day 18: Snailfish --- #
#############################

from itertools import permutations
from functools import reduce
import AOCUtils

def sum_left(n, i, to_sum):
    # Grab end of value
    e = i
    while e >= 0 and not n[e].isnumeric(): e -= 1
    if e < 0: return n # OOB, no value to add to

    # Find start of value
    s = e
    if n[s-1].isnumeric(): s -= 1 # May be two digits
    e += 1

    # Sum to value and replace it
    new = int(n[s:e]) + to_sum
    return n[:s] + str(new) + n[e:]

def sum_right(n, i, to_sum):
    # Grab start of value
    s = i
    while s < len(n) and not n[s].isnumeric(): s += 1
    if s >= len(n): return n # OOB, no value to add to

    # Find end of value
    e = s
    if n[e+1].isnumeric(): e += 1 # May be two digits
    e += 1

    # Sum to value and replace it
    new = int(n[s:e]) + to_sum
    return n[:s] + str(new) + n[e:]

def explode_snailfish(n):
    level = 0
    for i in range(len(n)):
        if n[i] == '[': level += 1
        elif n[i] == ']': level -= 1

        if level < 5: continue

        # Grab pair start and end
        s = i
        e = i
        while n[e] != ']': e += 1
        e += 1

        # Eval pair
        pair = eval(n[s:e])
        
        # Replace pair with 0 
        n = n[:s] + '0' + n[e:]

        # Sum values
        n = sum_right(n, i+1, pair[1])
        n = sum_left(n, i-1, pair[0])

        return True, n

    return False, n

def split_snailfish(n):
    for i in range(len(n)-1):
        s, e = i, i+2 # Assumes value will always be two digits

        if not n[s:e].isnumeric(): continue
        
        old = int(n[s:e])
        a = old // 2
        b = old - a

        n = n[:s] + f'[{a},{b}]' + n[e:]
        return True, n

    return False, n

def reduce_snailfish(n):
    n = str(n).replace(' ', '')

    while True:
        did_something, n = explode_snailfish(n)
        if did_something: continue

        did_something, n = split_snailfish(n)
        if not did_something: break

    return eval(n)

def add_snailfish(a, b):
    return reduce_snailfish([a, b])

def magnitude(n):
    if isinstance(n, int):
        return n

    return 3 * magnitude(n[0]) + 2 * magnitude(n[1])

#############################

snailfish_numbers = list(map(eval, AOCUtils.load_input(18)))

final_sum = reduce(add_snailfish, snailfish_numbers)

final_magnitude = magnitude(final_sum)
print(f'Part 1: \'{final_magnitude}\'')

max_magnitude = max(magnitude(add_snailfish(a, b)) for a, b in permutations(snailfish_numbers, 2))
print(f'Part 2: \'{max_magnitude}\'')

AOCUtils.print_time_taken()