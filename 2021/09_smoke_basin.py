##############################
# --- Day 9: Smoke Basin --- #
##############################

from collections import deque
import AOCUtils

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_low_points(cave):
    low_points = []
    for x in range(cave_size_x):
        for y in range(cave_size_y):
            higher_neighbors_amt = 0
            for dx, dy in directions:
                nxt_x, nxt_y = x + dx, y + dy

                # Count OOB as higher neighbor as well
                if not (0 <= nxt_x < cave_size_x and 0 <= nxt_y < cave_size_y):
                   higher_neighbors_amt += 1
                elif cave[nxt_x][nxt_y] > cave[x][y]:
                    higher_neighbors_amt += 1

            if higher_neighbors_amt == len(directions):
                low_points.append((x, y))

    return low_points

def get_basin_size(cave, low_point):
    queue = deque([low_point])
    visited = set()
    while queue:
        x, y = queue.popleft()

        if (x, y) in visited: continue
        visited.add((x, y))

        for dx, dy in directions:
            nxt_x, nxt_y = x + dx, y + dy

            # Skip if OOB
            if not (0 <= nxt_x < cave_size_x and 0 <= nxt_y < cave_size_y): continue

            # Skip if not higher than current
            if not (cave[nxt_x][nxt_y] > cave[x][y]): continue

            # Skip 9s
            if cave[nxt_x][nxt_y] == 9: continue

            queue.append((nxt_x, nxt_y))

    return len(visited)

##############################

cave_size_y = 100

# My utils func read all lines as ints, so had to revert that
cave = [list(map(int, str(r).zfill(cave_size_y))) for r in AOCUtils.load_input(9)]

cave_size_x = len(cave)
low_points = get_low_points(cave)

risk_levels = sum(1 + cave[i][j] for i, j in low_points)
AOCUtils.print_answer(1, risk_levels)

basin_sizes = [get_basin_size(cave, low_point) for low_point in low_points]
basin_sizes.sort(reverse=True)

p2 = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
AOCUtils.print_answer(2, p2)

AOCUtils.print_time_taken()