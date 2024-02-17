from copy import deepcopy
from collections import deque

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
        if 0 <= nx < 4 and 0 <= ny < 4 and not dieMonsters.get((nx, ny)) and (pi, pj) != (nx, ny):
            return (nx, ny), nk
        else:
            # 몬스터 시체가 있거나, 팩맨이 있는 경우거나 격자를 벗어나는 방향일 경우
            nk = (nk + 1) % 8
            cnt += 1
    # 움직일 수 없으면 유지
    return (x, y), k

# 팩맨 이동 함수
def movePacman(px, py):
    # 이동 후 팩맨 위치 
    pnx, pny = px, py
    # 이동 위치 저장
    route = set()
    # 몬스터 먹은 개수 저장
    maxV = -1
    # 상-좌-하-우의 우선순위
    deq = deque()
    # 현재 위치, 먹은 개수, 이동 경로 저장
    deq.append((px, py, 0, set()))
    # 이동 위치로 방문 체크
    visited = set()

    while deq:
        x, y, eatM, currRoute = deq.popleft()

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
                # 몬스터 개수
                mCnt = 0
                if (nx, ny) in newMonsters:
                    mCnt = len(newMonsters[(nx, ny)])

                deq.append((nx, ny, eatM + mCnt, nRoute))

    return pnx, pny, route


# 몬스터의 마리 수 m, 진행되는 턴의 수 t
m, t = map(int, input().split())
# 팩맨 위치
pi, pj = map(int, input().split())
pi -= 1
pj -= 1
# 살아있는 몬스터 저장 {(i, j): [d], ...}
monsters = dict()
# 몬스터 시체 수 저장 {위치: [방향, ...], ...}
dieMonsters = dict()
# 몬스터 위치, 방향 추가
for _ in range(m):
    r, c, d = map(int, input().split())
    key = (r-1, c-1)
    d -= 1
    if key in monsters:
        monsters[key].append(d)
    else:
        monsters[key] =[d]

# 상 부터 반시계 방향
di = [-1, -1, 0, 1, 1, 1, 0, -1] 
dj = [0, -1, -1, -1, 0, 1, 1, 1]

for _ in range(t):
    # 1.몬스터 복제
    copyMonsters = deepcopy(monsters)

    # 이동한 몬스터 저장
    newMonsters = dict()
    # 2.몬스터 이동
    for key in monsters:
        while monsters[key]:
            d = monsters[key].pop()
            newKey, nd = moveMonster(key[0], key[1], d)
            # 몬스터 이동 위치 추가
            if newKey in newMonsters:
                newMonsters[newKey].append(nd)
            else:
                newMonsters[newKey] =[nd]

    # 3.팩맨 이동
    pi, pj, moveRoute = movePacman(pi, pj)
    # 몬스터 먹기, 시체 생성
    for key in moveRoute:
        if newMonsters.get(key):
            # 몬스터 먹힘
            del newMonsters[key]
            # 시체 생성
            dieMonsters[key] = 2

    # 4.몬스터 시체 소멸
    delM = []
    for key, value in dieMonsters.items():
        if value == 1:
            delM.append(key)
            continue
        dieMonsters[key] -= 1
    # 완전 소멸
    for key in delM:
        del dieMonsters[key]
        
    monsters = newMonsters
    # 5.몬스터 복제 완성 (알 부화)            
    for key, value in copyMonsters.items():
        # 부화한 몬스터 위치 추가
        if key in monsters:
            monsters[key].extend(value)
        else:
            monsters[key] = value       

# 살아남은 몬스터 개수
ans = 0
for key in monsters:
    ans += len(monsters[key])
print(ans)