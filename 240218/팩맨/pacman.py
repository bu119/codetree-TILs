from copy import deepcopy

# 몬스터 이동
def move_monster():
    new_monster = [[[] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            while monsters[i][j]:
                move_d = monsters[i][j].pop()
                move_i, move_j = i, j
                for k in range(8):
                    nd = (move_d + k) % 8
                    ni = i + di[nd]
                    nj = j + dj[nd]
                    if 0 <= ni < 4 and 0 <= nj < 4 and monster_corpse[ni][nj] == 0 and pacman != [ni, nj]:
                        move_d = nd
                        move_i = ni
                        move_j = nj
                        break
                new_monster[move_i][move_j].append(move_d)
    return new_monster

# 팩맨 이동
def move_pacman():
    dfs(0, 0, pacman[0], pacman[1])

    for i, j in pacman_route:
        monsters[i][j] = []
        # 시체가 소멸되기 까지는 총 두 턴을 필요
        # ///// 소멸을 한턴이 끝나기 전에 실행하므로 2가 아니라 3을 해줘야한다. /////
        monster_corpse[i][j] = 3

def dfs(cnt, eat, i, j):
    global pacman, maxEat, pacman_route, route
    
    if cnt == 3:
        if maxEat < eat:
            maxEat = eat
            pacman = (i, j)
            pacman_route = deepcopy(route)
        return

    for k in [0, 2, 4, 6]:
        ni = i + di[k]
        nj = j + dj[k]
        if 0 <= ni < 4 and 0 <= nj < 4:
            # 몬스터 개수 확인
            # 이미 지난 칸이면 몬스터 없지~
            monster_cnt = 0
            if (ni, nj) not in route:
                monster_cnt = len(monsters[ni][nj])

            route.append((ni, nj))
            dfs(cnt+1, eat + monster_cnt, ni, nj)
            route.pop()

# 시체 소멸 & 복제 완성 (알 부화)
def extinction_and_hatching():
    for i in range(4):
        for j in range(4):
            if monster_corpse[i][j]:
                monster_corpse[i][j] -= 1
            if monster_clone[i][j]:
                monsters[i][j].extend(monster_clone[i][j])


m, t = map(int, input().split())
r, c = map(int, input().split())
pacman = [r-1, c-1]
monsters = [[[] for _ in range(4)] for _ in range(4)]
for _ in range(m):
    r, c, d = map(int, input().split())
    monsters[r-1][c-1].append(d-1)

# 몬스터 시체 수 저장
monster_corpse = [[0]*4 for _ in range(4)]
# ↑, ↖, ←, ↙, ↓, ↘, →, ↗
di = [-1,-1,0,1,1,1,0,-1]
dj = [0,-1,-1,-1,0,1,1,1]

for _ in range(t):
    #1.몬스터 복제
    monster_clone = deepcopy(monsters)
    #2.몬스터 이동
    monsters = move_monster()
    #3.팩맨 이동
    maxEat = -1
    # 최종 경로
    pacman_route = []
    # 계속 변경
    route = []
    move_pacman()
    #4.몬스터 시체 소멸 & 5.몬스터 복제 완성
    extinction_and_hatching()

answer = 0
for x in range(4):
    for y in range(4):
        answer += len(monsters[x][y])
print(answer)