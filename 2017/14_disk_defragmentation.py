########################################
# --- Day 14: Disk Defragmentation --- #
########################################

import AOCUtils

def knot_hash(string):
    circle = list(range(256))
    string = [ord(c) for c in string] + [17, 31, 73, 47, 23]
    cur = 0
    skip = 0

    for _ in range(64):
        for length in string:
            a = cur % len(circle)
            b = (cur + length) % len(circle)

            if b >= a:
                circle[a:b] = circle[a:b][::-1]
            else:
                s = (circle[a:] + circle[:b])[::-1]
                circle[a:] = s[:len(circle)-a]
                circle[:b] = s[len(circle)-a:]

            cur += length + skip
            skip += 1

    dense = []
    for i in range(16):
        dense.append(0)
        for j in range(16):
            dense[-1] ^= circle[16*i + j]

    return ''.join(hex(n)[2:].zfill(2) for n in dense)

def in_region(used_squares, p):
    region = set()

    def dfs(p):
        x, y = p
        if not (0 <= x < 128 and 0 <= y < 128): return
        if (x, y) not in used_squares: return
        if p in region: return

        region.add(p)

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            dfs((p[0]+dx, p[1]+dy))

    dfs(p)
    return region

########################################

key = AOCUtils.load_input(14)

grid = [bin(int(knot_hash(key+'-'+str(row)), 16))[2:].zfill(128) for row in range(128)]

used_squares = [(x, y) for x in range(128) for y in range(128) if grid[x][y] == '1']

AOCUtils.print_answer(1, len(used_squares))

total_regions = 0
not_seen = set(used_squares)
while not_seen:
    not_seen -= in_region(used_squares, not_seen.pop())
    total_regions += 1

AOCUtils.print_answer(2, total_regions)

AOCUtils.print_time_taken()