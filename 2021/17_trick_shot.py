##############################
# --- Day 17: Trick Shot --- #
##############################

from math import sqrt, ceil
import AOCUtils

def probe_reaches_target(velocity, target):
    vx, vy = velocity
    tx, ty = target
    px, py = 0, 0

    while True:
        # Stop simulation if:
        #  Probe is falling and target is above it.
        if vy < 0 and py < ty[0]: return None
        #  vx converges to 0 and x=0 is not in target.
        if vx == 0 and not (tx[0] <= px <= tx[1]): return None
        #  vx is neg/pos and target is to the right/left.
        if (vx < 0 and px < tx[0]) or (vx > 0 and px > tx[1]): return None

        # Update position and velocity
        px += vx
        py += vy

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        
        vy -= 1

        if tx[0] <= px <= tx[1] and ty[0] <= py <= ty[1]:
            return True

##############################

# Although all inputs seem to have target > x=0 and target < y=0 (quadrant IV),
#  this solution tries to make it work for any target at all, in any quadrant,
#  so it's definitely way more complex than needed, as it tries to be more general.

raw_target = AOCUtils.load_input(17)

target = ''.join(raw_target.split()[2:]).split(',')
target = tuple(tuple(map(int, ax[2:].split('..'))) for ax in target)

# Max height happens when max vy happens.
# Max vy is farthest edge of target, as any more than that would
#  overshoot (see v_lim_y upper bound comment below), and I am
#  always able to choose an arbitrary vx so that this holds true.
# However, if target <= y=0, the probe falls and reaches y=0
#  with y-velocity = -vy, its next step is y-velocity = -vy-1,
#  so it overshoots the target by exactly one unit.
# In that case, max_abs_vy is [the target abs max y - 1].
# If I considered only targets in quadrant IV, max_abs_vy == abs(target[1][0])-1.
max_abs_vy = max(abs(target[1][0])-1, abs(target[1][1]))

max_y = (max_abs_vy * (max_abs_vy + 1)) // 2
AOCUtils.print_answer(1, max_y)

# Probe only reaches the target if:
#  [vx has the same sign as target closest edge] and
#  [vx is at least X so its triangular number reaches target]
#              ^
#              or at most, for targets < x=0

# Triangular number to reach target means (swap '>=' with '<=' for targets < x=0):
#   (X + X**2) // 2 >= target closest edge ===
#   (X+X**2)//2 >= tce ===
#   X >= ceil((-1 + sqrt(1 + 8*tce)) / 2)

if target[0][0] >= 0: # target >= x=0
    target_closest_edge = target[0][0]
    min_vx_to_reach_target = ceil((-1 + sqrt(1 + 8 * target_closest_edge)) / 2)
    
    min_vx = min_vx_to_reach_target
    max_vx = target[0][1]
else: # target < x=0
    target_closest_edge = target[0][1]
    max_vx_to_reach_target = ceil((-1 + sqrt(1 + 8 * target_closest_edge)) / 2)
    
    min_vx = target[0][0]
    max_vx = max(max_vx_to_reach_target, target[0][1])

#  As vy is always decreasing:
#   If target < y=0, vy can't be lower than the bottom of target.
#   If target >= y=0, vy >= 0.
min_vy = min(0, target[1][0])

#  vy can't be higher than the target max abs y, as its trajectory
#   would overshoot the target regardless of being above/below y=0,
#   and regardless of it (potentially) reaching target when
#   rising or falling, as the y-trajectory is symmetric.
max_vy = max(abs(target[1][0]), abs(target[1][1]))

hits = 0
for vx in range(min_vx, max_vx+1):
    for vy in range(min_vy, max_vy+1):
        velocity = (vx, vy)

        if probe_reaches_target(velocity, target):
            hits += 1

AOCUtils.print_answer(2, hits)

AOCUtils.print_time_taken()