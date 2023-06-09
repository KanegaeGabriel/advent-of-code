#############################
# --- Day 18: Snailfish --- #
#############################

from itertools import permutations
from functools import reduce
from collections import namedtuple
import AOCUtils

Element = namedtuple('Element', ['val', 'level'])

def explode_snailfish(n):
    for i, x in enumerate(n[:-1]):
        if x.level < 5:
            continue

        j = i+1
        y = n[j]

        insert = []
        if i > 0:
            left = n[i-1]
            insert.append(Element(left.val + x.val, left.level))
        insert.append(Element(0, x.level-1))
        if j < len(n)-1:
            right = n[j+1]
            insert.append(Element(right.val + y.val, right.level))

        n = n[:max(0, i-1)] + insert + n[j+1+1:]
        return True, n

    return False, n

def split_snailfish(n):
    for i, ele in enumerate(n):
        if ele.val < 10: continue

        a = Element(ele.val//2, ele.level+1)
        b = Element(ele.val - ele.val//2, ele.level+1)

        n = n[:i] + [a, b] + n[i+1:]
        return True, n

    return False, n

def reduce_snailfish(n):
    while True:
        did_something, n = explode_snailfish(n)
        if did_something: continue

        did_something, n = split_snailfish(n)
        if not did_something: break

    return n

def add_snailfish(a, b):
    c = [Element(ele.val, ele.level+1) for ele in a+b]
    return reduce_snailfish(c)

def flatten_snalfish_number(n):
    flat_n = []

    level = 0
    for i in range(len(n)):
        if n[i] == '[': level += 1
        elif n[i] == ']': level -= 1
        
        j = i
        while j < len(n) and n[j].isnumeric():
            j += 1

        if j != i:
            ele = Element(int(n[i:j]), level)
            flat_n.append(ele)

    return flat_n

def magnitude(n):
    to_be_done = list(reversed(n))
    stack = []

    while to_be_done:
        stack.append(to_be_done.pop())
        while len(stack) > 1 and stack[-1].level == stack[-2].level:
            cur = stack.pop()
            prev = stack.pop()

            new = Element(3 * prev.val + 2 * cur.val, cur.level - 1)
            stack.append(new)

    return stack[0].val

#############################

raw_snailfish_numbers = AOCUtils.load_input(18)

snailfish_numbers = list(map(flatten_snalfish_number, raw_snailfish_numbers))

final_sum = reduce(add_snailfish, snailfish_numbers)

final_magnitude = magnitude(final_sum)
AOCUtils.print_answer(1, final_magnitude)

max_magnitude = max(magnitude(add_snailfish(a, b)) for a, b in permutations(snailfish_numbers, 2))
AOCUtils.print_answer(2, max_magnitude)

AOCUtils.print_time_taken()