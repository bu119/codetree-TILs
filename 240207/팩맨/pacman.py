from copy import deepcopy

def moveMonster(x, y, k):
    nk = k
    cnt = 1
    while cnt < 9:
        nx = x + di[nk]
        ny = y + dj[nk]
        if not (0 <= nx < 4 and 0 <= ny < 4) or dieMonsters[nx][ny] > 0 or (pi == nx and pj == ny):
            nk = (nk + 1) % 8
            cnt += 1
        else:
            # 이등 조건을 만족하면
            return nx, ny, nk
    # 모두 움직일 수 없었다면 그대로
    return x, y, k


def movePacman(x, y):
    global pi, pj

    visited = set()
    stack = [(x, y, 0, set())]
    route = set()
    maxV = 0
    while stack:
        x, y, eat, currRoute = stack.pop()

        if len(currRoute) == 3:
            if maxV < eat:
                maxV = eat
                route = currRoute
                pi, pj = x, y

        # 상 좌 하 우
        for k in [0, 2, 4, 6]:
            nx = x + di[k]
            ny = y + dj[k]
            if 0 <= nx < 4 and 0 <= ny < 4 and (nx, ny) not in currRoute:
                nRoute = deepcopy(currRoute)
                nRoute.add((nx, ny))
                if nRoute not in visited:
                    stack.append((nx, ny, eat + liveMonster[nx][ny], nRoute))

    return route





# 몬스터의 마리 수 m, 진행되는 턴의 수 t
m, t = map(int, input().split())
# pacman
pi, pj = map(int, input().split())
# i, j, d
monsters = []
# 살아있는 몬스터 개수 저장
liveMonster = [[0]*4 for _ in range(4)]

for _ in range(m):
    r, c, d = map(int, input().split())
    r -= 1
    c -= 1
    monsters.append((r, c, d-1))
    liveMonster[r][c] += 1

# 상 부터 반시계 방향
di = [-1, -1, 0, 1, 1, 1, 0, -1] 
dj = [0, -1, -1, -1, 0, 1, 1, 1]

# 죽은 몬스터 시체 저장
dieMonsters = [[0]*4 for _ in range(4)]
for _ in range(t):
    # 몬스터 복제
    copyMonsters = deepcopy(monsters)
    newMonsters = []
    # 몬스터 이동
    for i, j, d in monsters:
        liveMonster[i][j] -= 1
        ni, nj, nd = moveMonster(i, j, d)
        newMonsters.append((ni, nj, nd))
        liveMonster[ni][nj] += 1
    moveRoute = movePacman(pi, pj)
    # 시체 생성
    for i, j in moveRoute:
        dieMonsters[i][j] += 2
        liveMonster[i][j] = 0
    # 시체 소멸
    for i in range(4):
        for j in range(4):
            if dieMonsters[i][j] > 0:
                dieMonsters[i][j] -= 1
    # 알 부화            
    for i, j, d in copyMonsters:
        liveMonster[i][j] += 1
    
    monsters = newMonsters + copyMonsters


ans = 0
for i in range(4):
    ans += sum(liveMonster[i])
print(ans)