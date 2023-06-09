#################################
# --- Day 10: Adapter Array --- #
#################################

import AOCUtils

#################################

adapters = AOCUtils.load_input(10)

adapters.sort()

j1, j3 = 0, 0
cur = 0
for n in adapters:
    delta = n - cur

    j1 += int(delta == 1)
    j3 += int(delta == 3)

    cur += delta

j3 += 1

AOCUtils.print_answer(1, j1 * j3)

memo = [0] * (max(adapters) + 1)
memo[0] = 1

for n in adapters:
    l1 = memo[n-1] if n-1 >= 0 else 0
    l2 = memo[n-2] if n-2 >= 0 else 0
    l3 = memo[n-3] if n-3 >= 0 else 0

    memo[n] = l1 + l2 + l3

AOCUtils.print_answer(2, memo[-1])

AOCUtils.print_time_taken()