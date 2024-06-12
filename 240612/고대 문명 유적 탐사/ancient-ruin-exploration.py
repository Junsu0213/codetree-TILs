import sys
import copy
from collections import deque
input = sys.stdin.readline

k, m = map(int, input().split())

visited = [[False]*5 for _ in range(5)]

map_list = [[] for _ in range(5)]

for i in range(5):
    m_list = map(int, input().split())
    for num in m_list:
        map_list[i].append(num)

q = deque()

wall_list = map(int, input().split())
for w in wall_list:
    q.append(w)


def spin_90 (map_list, center_point):
    x, y = center_point
    x -= 2
    y -= 2
    map_ch = copy.deepcopy(map_list)
    map_ch[x+0][y+0] = map_list[x+2][y+0]
    map_ch[x+0][y+1] = map_list[x+1][y+0]
    map_ch[x+0][y+2] = map_list[x+0][y+0]
    map_ch[x+1][y+2] = map_list[x+0][y+1]
    map_ch[x+2][y+2] = map_list[x+0][y+2]
    map_ch[x+2][y+1] = map_list[x+0][y+1]
    map_ch[x+2][y+0] = map_list[x+2][y+2]
    map_ch[x+1][y+0] = map_list[x+2][y+1]
    return map_ch

def spin_180 (map_list, center_point):
    x, y = center_point
    x -= 2
    y -= 2
    map_ch = copy.deepcopy(map_list)
    map_ch[x+0][y+0] = map_list[x+2][y+2]
    map_ch[x+0][y+1] = map_list[x+2][y+1]
    map_ch[x+0][y+2] = map_list[x+2][y+0]
    map_ch[x+1][y+2] = map_list[x+1][y+0]
    map_ch[x+2][y+2] = map_list[x+0][y+0]
    map_ch[x+2][y+1] = map_list[x+0][y+1]
    map_ch[x+2][y+0] = map_list[x+0][y+2]
    map_ch[x+1][y+0] = map_list[x+1][y+2]
    return map_ch

def spin_270 (map_list, center_point):
    x, y = center_point
    x -= 2
    y -= 2
    map_ch = copy.deepcopy(map_list)
    map_ch[x+0][y+0] = map_list[x+0][y+2]
    map_ch[x+0][y+1] = map_list[x+1][y+2]
    map_ch[x+0][y+2] = map_list[x+2][y+2]
    map_ch[x+1][y+2] = map_list[x+2][y+1]
    map_ch[x+2][y+2] = map_list[x+2][y+0]
    map_ch[x+2][y+1] = map_list[x+1][y+0]
    map_ch[x+2][y+0] = map_list[x+0][y+0]
    map_ch[x+1][y+0] = map_list[x+0][y+1]
    return map_ch


def u_acq(map_list, visited):
    dy = [1, -1, 0, 0]
    dx = [0, 0, 1, -1]
    qq = deque()

    total_stack = 0
    total_visited = copy.deepcopy(visited)

    for row in range(5):
        for col in range(5):
            
            if total_visited[row][col] == False:
                qq.append([row, col])
            
            visited_ = [[False]*5 for _ in range(5)]
            stack = 1
            idx = map_list[row][col]
            visited_[row][col] = True

            while qq:
                y_, x_ = qq.popleft()

                for ii in range(4):
                    dy_ = y_ + dy[ii]
                    dx_ = x_ + dx[ii]

                    if 0 <= dy_ < 5 and 0 <= dx_ < 5 and idx == map_list[dy_][dx_] and visited_[dy_][dx_] == False:
                        stack += 1
                        visited_[dy_][dx_] = True
                        qq.append([dy_, dx_])

            if stack >= 3:
                total_stack += stack
                for row_ in range(5):
                    for col_ in range(5):
                        if visited_[row_][col_] == True:
                            total_visited[row_][col_] = True
    return total_stack, total_visited

result = 0

while k > 0:
    max_num = 0
    stack_list = []
    center_point_list = []
    for cen_col in range(2, 5):
        for cen_row in range(2, 5):
            center_point = [cen_row, cen_col]

            map_90 = spin_90(map_list, center_point)
            map_180 = spin_180(map_list, center_point)
            map_270 = spin_270(map_list, center_point)

            stack_90, _ = u_acq(map_90, visited)
            stack_180, _ = u_acq(map_180, visited)
            stack_270, _ = u_acq(map_270, visited)
            stack_list.append([stack_90, stack_180, stack_270])
            center_point_list.append(center_point)
            max_n = max(stack_90, stack_180, stack_270)
            max_num = max(max_num, max_n)

    first_spin = False
    for s in range(3):
        for c in range(9):
            if max_num == stack_list[c][s]:
                center_point = center_point_list[c]
                first_spin = True
                spin_degree = s
                break
            if first_spin is True:
                break
    if spin_degree == 0:
        map_spin = spin_90(map_list, center_point)
        _, total_visited = u_acq(map_spin, visited)
    elif spin_degree == 0:
        map_spin = spin_180(map_list, center_point)
        _, total_visited_ = u_acq(map_spin, visited)
    else:
        map_spin = spin_270(map_list, center_point)
        _, total_visited = u_acq(map_spin, visited)
    
    if max_num > len(q):
        break

    result += max_num
    
    while True:

        for col in range(5):
            for row in range(4, -1, -1):
                if total_visited[row][col] == True:
                    try:
                        map_spin[row][col] = q.popleft()
                    except:
                        break

        stack, total_visited = u_acq(map_spin, visited)

        result += stack
        if stack == 0:
            break
    k -= 1

print(result)