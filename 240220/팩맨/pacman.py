from copy import deepcopy

# 몬스터 이동
def move_monster():
    new_monster = [[[] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for move_d in monsters[i][j]:
                move_i, move_j = i, j
                for k in range(8):
                    nd = (move_d + k) % 8
                    ni = i + di[nd]
                    nj = j + dj[nd]
                    if 0 <= ni < 4 and 0 <= nj < 4 and monster_corpse[ni][nj] == 0 and (pi, pj) != (ni, nj):
                        move_d = nd
                        move_i = ni
                        move_j = nj
                        break
                new_monster[move_i][move_j].append(move_d)
    return new_monster

# 팩맨 이동
def move_pacman():
    global pi, pj
    # 팩맨 이동 방향
    pacman_route = find_pacman_route()
    # 팩맨 이동
    for k in pacman_route:
        pi += di[k]
        pj += dj[k]
        # ///// 몬스터 있을 때만 실행 /////
        if monsters[pi][pj]:
            monsters[pi][pj] = []
            # 시체가 소멸되기 까지는 총 두 턴을 필요
            # ///// 소멸을 한턴이 끝나기 전에 실행하므로 2가 아니라 3을 해줘야한다. /////
            monster_corpse[pi][pj] = 3

# 팩맨 이동 방향 찾기
def find_pacman_route():
    # 최대 먹은 몬스터 수
    maxEat = -1
    # 경로
    route_dir = (-1, -1, -1)
    # 우선순위 순서대로 이동
    for d1 in [0, 2, 4, 6]:
        for d2 in [0, 2, 4, 6]:
            for d3 in [0, 2, 4, 6]:
                # 죽은 몬스터 수 저장
                eat = dead_monster(d1, d2, d3)
                # 최대값 갱신
                if maxEat < eat:
                    maxEat = eat
                    route_dir = (d1, d2, d3)
    return route_dir

# 죽은 몬스터 개수 찾기
def dead_monster(dir1, dir2, dir3):
    ni, nj = pi, pj
    # 몬스터 개수 저장
    cnt = 0
    # 방문 체크
    visited = set()
    for k in [dir1, dir2, dir3]:
        ni += di[k]
        nj += dj[k]
        if not (0 <= ni < 4 and 0 <= nj < 4):
            return -1
        # ///// 이미 지난 칸이면 몬스터 없지~ /////
        if (ni, nj) not in visited:
            cnt += len(monsters[ni][nj])
            visited.add((ni, nj))
    return cnt

# 시체 소멸 & 복제 완성 (알 부화)
def extinction_and_hatching():
    for i in range(4):
        for j in range(4):
            if monster_corpse[i][j] > 0:
                monster_corpse[i][j] -= 1
            if monster_clone[i][j]:
                monsters[i][j].extend(monster_clone[i][j])


m, t = map(int, input().split())
r, c = map(int, input().split())
pi = r-1
pj = c-1
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
    move_pacman()
    #4.몬스터 시체 소멸 & 5.몬스터 복제 완성
    extinction_and_hatching()

answer = 0
for x in range(4):
    for y in range(4):
        answer += len(monsters[x][y])
print(answer)