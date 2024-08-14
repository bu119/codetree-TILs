#  n * n 크기의 격자 정보
# 0은 빈 공간
# 1은 사무실 구역
# 2는 에어컨이 놓여있으며 왼쪽 방향을 향하고 있음
# 3은 에어컨이 놓여있으며 위를 향하고 있음
# 4는 에어컨이 놓여있으며 오른쪽을 향하고 있음
# 5는 에어컨이 놓여있으며 아래를 향하고 있음
from copy import deepcopy

def turn_on(sx, sy, direction):

    nx = sx + di[direction]
    ny = sy + dj[direction]

    stack = [(nx, ny, 5)]
    visited[nx][ny] = 1

    while stack:
        x, y, level = stack.pop()

        if level == 0:
            continue

        airLevel[x][y] += level

        # 다음 방향으로 갈 수 있는 지 체크
        # 직진: straight
        nx, ny = go_straight(x, y, direction)
        if nx >= 0:
            stack.append((nx, ny, level-1))
        # 45_1
        nx, ny = go_up_and_left_45(x, y, direction)
        if nx >= 0:
            stack.append((nx, ny, level-1))
        # 45_2
        nx, ny = go_down_and_right_45(x, y, direction)
        if nx >= 0:
            stack.append((nx, ny, level-1))

# 벽 체크
def check_wall(x, y, move):
    nx = x
    ny = y
    for d in move:
        if (nx, ny, d) not in wall:
            nx += di[d]
            ny += dj[d]
            if not (0 <= nx < n and 0 <= ny < n and visited[nx][ny] == 0):
                return -1, -1

    visited[nx][ny] = 1
    return nx, ny

# 2:좌, 3: 상, 4: 우, 5: 하
def go_straight(x, y, direction):

    if (x, y, direction) not in wall:
        nx = x + di[direction]
        ny = y + dj[direction]
        if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == 0:
            visited[nx][ny] = 1
            return nx, ny
    return -1, -1


# 위쪽, 왼쪽 45
def go_up_and_left_45(x, y, direction):
    
    # 좌: 상 -> 좌
    if direction == 2:
        return check_wall(x, y, [3, 2])
    # 상: 좌 -> 상
    elif direction == 3:
        return check_wall(x, y, [2, 3])
    # 우: 상 -> 우   
    elif direction == 4:
        return check_wall(x, y, [3, 4])
    # 하: 좌 -> 하
    else:
        return check_wall(x, y, [2, 5])

# 아래쪽, 오른쪽 45
def go_down_and_right_45(x, y, direction):
    # 좌: 하 -> 좌
    if direction == 2:
        return check_wall(x, y, [5, 2])
    # 상: 우 -> 상
    elif direction == 3:
        return check_wall(x, y, [4, 3])
    # 우: 하 -> 우   
    elif direction == 4:
        return check_wall(x, y, [5, 4])
    # 하: 우 -> 하
    else:
        return check_wall(x, y, [4, 5])


# 공기를 섞는 함수
def mix_air():
    # air_diff = [[0] * n for _ in range(n)]
    air = deepcopy(airLevel)
    # 덜 시원한 쪽에서 체크
    for i in range(n):
        for j in range(n):
            # 좌, 상 방향만 체크 (중복방지)
            for d in [2, 3]:
                # 벽 체크
                if (i, j, d) not in wall:
                    ni = i + di[d]
                    nj = j + dj[d]
                    if 0 <= ni < n and 0 <= nj < n:
                        diff = abs(airLevel[ni][nj] - airLevel[i][j]) // 4
                        # 시원함이 높은 곳에서 낮은 곳으로 공기 읻오
                        if airLevel[i][j] < airLevel[ni][nj]:
                            air[ni][nj] -= diff
                            air[i][j] += diff
                        elif airLevel[i][j] > airLevel[ni][nj]:
                            air[i][j] -= diff
                            air[ni][nj] += diff
    return air


# 외벽에 있는 칸에 대해서만 시원함이 1씩 감소시키는 함
def touch_outer_wall():
    for i in range(n):
        for j in [0, n-1]:
            # 0 또는 n-1로 행 고정
            if airLevel[i][j] > 0:
                airLevel[i][j] -= 1
            # 0 또는 n-1로 열 고정
            # (0, 0), (n-1, n-1)은 두 번 되므로 여기서는 제외
            if 0 < i < n-1 and airLevel[j][i] > 0:
                airLevel[j][i] -= 1        

# 사무실이 모두 시원해 졌는지 확인하는 함수
def is_all_cool():
    for x, y in office:
        if airLevel[x][y] < k:
            return False
    return True


n, m, k = map(int, input().split())
airLevel = [[0]*n for _ in range(n)]
board = []
office = []
airConditioner = []
for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        if row[j] == 1:
            office.append((i, j))
        elif row[j] != 0:
            airConditioner.append((i, j, row[j]))
    board.append(row)

# 2:좌, 3: 상, 4: 우, 5: 하
di = [0, 0, 0, -1, 0, 1]
dj = [0, 0, -1, 0, 1, 0]

# 현재 위치에서 이동 방향에 따라 벽이 있음을 나타냄
wall = set()
for _ in range(m):
    x, y, s = map(int, input().split())
    if s == 0:
        # (x, y) 바로 위에 벽 -> (x, y)에서 위로 갈 때, (x-1, y)에서 아래로 갈 때
        wall.add((x, y, 3))
        if 0 <= x-1:
            wall.add((x-1, y, 5))
    else:
        # (x, y) 바로 왼쪽에 벽 -> (x, y)에서 왼쪽으로 갈 때, (x, y-1)에서 오른쪽으로 갈 때
        wall.add((x, y, 2))
        if 0 <= y-1:
            wall.add((x, y-1, 4))


# 100분이 넘도록 사무실이 모두 시원하지 않다면 -1 출력
for t in range(1, 101):
    # 에어컨 실행
    for x, y, d in airConditioner:
        visited = [[0]*n for _ in range(n)]
        turn_on(x, y, d)
    # 시원한 공기들이 섞이기 시작
    airLevel = mix_air()
    # 외벽에 있는 칸에 대해서만 시원함이 1씩 감소
    touch_outer_wall()

    # 사무실이 모두 시원해 졌는지 체크
    if is_all_cool():
        print(t)
        break

if t > 100:
    print(-1)