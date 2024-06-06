import sys
input = sys.stdin.readline
from collections import deque


def bfs(visited, ri, ci):
    visited_ = [[False] * c for _ in range(r + 3)]
    x = [1, -1, 0, 0]
    y = [0, 0, -1, 1]
    q = deque()
    q.append((ri, ci))
    rmax = ri - 1
    while q:
        ri, ci = q.popleft()
        idx = visited[ri][ci]
        if idx == 3:
            rmax = max(rmax, ri - 1)
        visited_[ri][ci] = True

        for k in range(4):
            dx = ri + x[k]
            dy = ci + y[k]
            if 0 <= dx <= r+1 and 0 <= dy <= c-1 and (idx == 2 or idx == 3) and visited[dx][dy] != 0 and visited_[dx][dy] == False:
                visited_[dx][dy] = True
                q.append((dx, dy))
            elif 0 <= dx <= r+1 and 0 <= dy <= c-1 and idx == 1 and visited[dx][dy] == 3 and visited[dx][dy] != 0 and visited_[dx][dy] == False:
                visited_[dx][dy] = True
                q.append((dx, dy))
    return rmax


def g_down(visited, r, c, ci, di):
    ri = 0
    while True:
        gn, ge, gs, gw = visited[ri - 1][ci], visited[ri][ci + 1], visited[ri + 1][ci], visited[ri][ci - 1]

        # down
        if ge == 0 and gs == 0 and gw == 0:
            ri += 1
            if ri == r + 1 and visited[ri][ci + 1] == 0 and visited[ri + 1][ci] == 0 and visited[ri][ci - 1] == 0:
                break

        # left
        elif gs != 0 and gw == 0 and ci >= 2 and visited[ri + 1][ci - 1] == 0 and visited[ri][ci - 2] == 0:
            ci -= 1
            di -= 1
            if di < 0:
                di = 3

        # right
        elif gs != 0 and ge == 0 and ci <= c - 3 and visited[ri + 1][ci + 1] == 0 and visited[ri][
            ci + 2] == 0:
            ci += 1
            di += 1
            if di > 3:
                di = 0

        else:
            ri -= 1
            break

    # map reset
    if ri < 3:
        visited = [[0] * c for _ in range(r + 3)]
        rmax = 0

    else:
        visited[ri][ci] = 3
        visited[ri + 1][ci] = 1
        visited[ri - 1][ci] = 1
        visited[ri][ci + 1] = 1
        visited[ri][ci - 1] = 1

        if di == 0:
            visited[ri - 1][ci] = 2
        elif di == 1:
            visited[ri][ci + 1] = 2
        elif di == 2:
            visited[ri + 1][ci] = 2
        elif di == 3:
            visited[ri][ci - 1] = 2

        rmax = bfs(visited, ri, ci)

    return visited, rmax


r, c, k = map(int, input().split())
visited = [[0] * c for _ in range(r + 3)]

answer = 0
for _ in range(k):
    ci, di = map(int, input().split())
    ci -= 1
    visited, rmax = g_down(visited, r, c, ci, di)

    answer += rmax

print(answer)