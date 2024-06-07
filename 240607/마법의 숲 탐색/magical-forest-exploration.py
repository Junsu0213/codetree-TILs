import sys
from collections import deque

input = sys.stdin.readline


def bfs(maps, ri, ci):
    visited = [[False]*c for _ in range(r+2)]
    q = deque()
    q.append((ri, ci))
    dy = [1, -1, 0, 0]
    dx = [0, 0, 1, -1]
    rmax = ri

    while q:
        ri, ci = q.popleft()
        visited[ri][ci] = True
        idx = maps[ri][ci]
        if idx == 3:
            rmax = max(rmax, ri)

        for i in range(4):
            y = ri + dy[i]
            x = ci + dx[i]
            if 2 <= y < r+2 and 0 <= x < c and (idx == 3 or idx == 2) and maps[y][x] != 0 and visited[y][x] == False:
                q.append((y, x))
                visited[y][x] = True
            elif 2 <= y < r+2 and 0 <= x < c and idx == 1 and maps[y][x] == 3 and visited[y][x] == False:
                q.append((y, x))
                visited[y][x] = True
    return rmax 
     

def g_move(maps, r, c, ci, di):
    ri = 0

    while True:
        # stop
        if ri == r:
            break
        ge, gs, gw = maps[ri + 1][ci + 1], maps[ri + 2][ci], maps[ri + 1][ci - 1]        
        # down
        if ri < r and ge == 0 and gs == 0 and gw == 0:
            ri += 1
        # left
        elif ci > 1 and (gs != 0 or ge != 0) and gw == 0 and maps[ri][ci - 2] == 0 and maps[ri + 1][ci - 2] == 0 and maps[ri + 2][ci - 1] == 0:
            ci -= 1
            di -= 1
            if di < 0:
                di = 3
        # right
        elif ci < c - 2 and (gs != 0 or gw != 0) and ge == 0 and maps[ri][ci + 2] == 0 and maps[ri + 1][ci + 2] == 0 and maps[ri + 2][ci + 1] == 0:
            ci += 1
            di += 1
            if di > 3:
                di = 0
        else:
            break

    if ri < 3:
        maps = [[0]*c for _ in range(r+2)]
        rmax = 0
    else:
        maps[ri][ci] = 3
        maps[ri - 1][ci] = 1
        maps[ri][ci + 1] = 1
        maps[ri + 1][ci] = 1
        maps[ri][ci - 1] = 1
        
        # exit
        if di == 0:
            maps[ri - 1][ci] = 2
        elif di == 1:
            maps[ri][ci + 1] = 2
        elif di == 2:
            maps[ri + 1][ci] = 2
        elif di == 3:
            maps[ri][ci - 1] = 2
        
        rmax = bfs(maps, ri, ci)
    return maps, rmax


r, c, k = map(int, input().split())
maps = [[0]*c for _ in range(r+2)]
answer = 0

for _ in range(k):
    ci, di = map(int, input().split())
    maps, rmax = g_move(maps, r, c, ci - 1, di)
    answer += rmax

print(answer)