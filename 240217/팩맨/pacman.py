from copy import deepcopy

# 몬스터 이동 함수
def moveMonster(x, y, k):
    # 이동 방향
    nk = k
    # 회전 수 저장
    cnt = 0
    while cnt < 8:
        nx = x + di[nk]
        ny = y + dj[nk]
        # 격자에 위치하고 몬스터 시체와 팩맨이 없으면 이동할 수 있다.
        if 0 <= nx < 4 and 0 <= ny < 4 and dieMonsters[nx][ny] == 0 and (pi, pj) != (nx, ny):
            return nx, ny, nk
        else:
            # 몬스터 시체가 있거나, 팩맨이 있는 경우거나 격자를 벗어나는 방향일 경우
            nk = (nk + 1) % 8
            cnt += 1
    # 움직일 수 없으면 유지
    return x, y, k

# 팩맨 이동 함수
def movePacman(px, py):
    # 이동 후 팩맨 위치 
    pnx, pny = px, py
    # 이동 위치 저장
    route = set()
    # 몬스터 먹은 개수 저장
    maxV = 0
    
    # 현재 위치, 먹은 개수, 이동 경로 저장
    stack = [(px, py, 0, set())]
    # 이동 위치로 방문 체크
    visited = set()

    while stack:
        x, y, eatM, currRoute = stack.pop()

        # 방문 체크
        now = tuple(sorted(currRoute))
        if now in visited:
            continue
        visited.add(now)

        # 팩맨 3칸 이동 다하면 먹은 개수, 이동 경로, 팩맨 위치 갱신
        if len(currRoute) == 3:
            if maxV < eatM:
                maxV = eatM
                route = currRoute
                pnx, pny = x, y
            continue

        # 상 좌 하 우
        for k in [0, 2, 4, 6]:
            nx = x + di[k]
            ny = y + dj[k]
            if 0 <= nx < 4 and 0 <= ny < 4 and (nx, ny) not in currRoute:
                # 새로운 경로 저장
                nRoute = deepcopy(currRoute)
                nRoute.add((nx, ny))
                stack.append((nx, ny, eatM + liveMonster[nx][ny], nRoute))

    return pnx, pny, route


# 몬스터의 마리 수 m, 진행되는 턴의 수 t
m, t = map(int, input().split())
# 팩맨 위치
pi, pj = map(int, input().split())
pi -= 1
pj -= 1
# 살아있는 몬스터 수 저장
liveMonster = [[0]*4 for _ in range(4)]
# 몬스터 시체 수 저장
dieMonsters = [[0]*4 for _ in range(4)]
# 살아있는 몬스터 저장 (i, j, d)
monsters = []
# 몬스터 위치, 방향 추가
for _ in range(m):
    r, c, d = map(int, input().split())
    r -= 1
    c -= 1
    monsters.append((r, c, d-1))
    liveMonster[r][c] += 1

# 상 부터 반시계 방향
di = [-1, -1, 0, 1, 1, 1, 0, -1] 
dj = [0, -1, -1, -1, 0, 1, 1, 1]

for _ in range(t):
    # 1.몬스터 복제
    copyMonsters = deepcopy(monsters)

    # 몬스터 이동 위치 저장
    newMonsters = []
    # 2.몬스터 이동
    for i, j, d in monsters:
        liveMonster[i][j] -= 1
        ni, nj, nd = moveMonster(i, j, d)
        # 몬스터 이동 위치 추가
        newMonsters.append((ni, nj, nd))
        liveMonster[ni][nj] += 1

    # 3.팩맨 이동
    pi, pj, moveRoute = movePacman(pi, pj)
    # 몬스터 먹기, 시체 생성
    for i, j in moveRoute:
        # 몬스터 먹힘
        liveMonster[i][j] = 0
        # 시체 생성
        dieMonsters[i][j] = 2
        
    # 살아있는 몬스터 저장
    monsters = []
    for i, j, d in newMonsters:
        if (i, j) not in moveRoute:
            monsters.append((i, j, d))     

    # 4.몬스터 시체 소멸
    for i in range(4):
        for j in range(4):
            if dieMonsters[i][j] > 0:
                dieMonsters[i][j] -= 1

    # 5.몬스터 복제 완성 (알 부화)            
    for i, j, d in copyMonsters:
        liveMonster[i][j] += 1
        # 부화한 몬스터 위치 추가
        monsters.append((i, j, d))

# 살아남은 몬스터 개수
ans = 0
for i in range(4):
    ans += sum(liveMonster[i])
print(ans)