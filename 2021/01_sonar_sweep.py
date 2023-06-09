##############################
# --- Day 1: Sonar Sweep --- #
##############################

import AOCUtils

##############################

depths = AOCUtils.load_input(1)

increases = 0
for i in range(1, len(depths)):
    if depths[i-1] < depths[i]:
        increases += 1

AOCUtils.print_answer(1, increases)

increases = 0
for i in range(1, len(depths)-2):
    cur = depths[i-1] + depths[i] + depths[i+1]
    nxt = depths[i] + depths[i+1] + depths[i+2]
    if cur < nxt:
        increases += 1

AOCUtils.print_answer(2, increases)

AOCUtils.print_time_taken()