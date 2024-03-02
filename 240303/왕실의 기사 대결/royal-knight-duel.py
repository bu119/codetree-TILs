# 체스판의 왼쪽 상단은 (1,1)로 시작, 
# 빈칸, 함정, 또는 벽 구성, 체스판 밖도 벽
# 기사: (r,c)를 좌측 상단으로 하며 h(높이)×w(너비) 크기의 직사각형, 각 기사의 체력은 k
# (1) 기사 이동
# 상하좌우 중 하나로 한 칸 이동
# 1. 다른 기사가 있다면 그 기사도 함께 연쇄적으로 한 칸 밀려나게 됩니다.
# 그 옆에 또 기사가 있다면 연쇄적으로 한 칸씩 밀리게 됩니다.
# 2. 기사가 이동하려는 방향의 끝에 벽이 있다면 모든 기사는 이동할 수 없게 됩니다.
# 3. 체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없게 됩니다.
# (2) 대결 대미지
# 1. 명령을 받은 기사가 다른 기사를 밀치게 되면, 밀려난 기사들은 피해를 입게 됩니다. 
# 2. 해당 기사가 이동한 곳에서 w×h 직사각형 내에 놓여 있는 함정의 수만큼만 피해를 입게 됩니다.
# 3. 피해를 받은 만큼 체력이 깎이게 되며
# 4. 현재 체력 이상의 대미지를 받을 경우 기사는 체스판에서 사라지게 됩니다. 
# 5.명령을 받은 기사는 피해를 입지 않으며, 기사들은 모두 밀린 이후에 대미지를 입게 됩니다. 
# 6.밀렸더라도 밀쳐진 위치에 함정이 전혀 없다면 그 기사는 피해를 전혀 입지 않게 됨에 유의합니다.
from copy import deepcopy
from collections import deque

def can_move(starter, other):
    global new_knights, new_knightsInfo

    r, c, h, w, k, damage = new_knightsInfo[other]
    # 변한 위치 변경
    new_knightsInfo[other][0] = r + di[d]
    new_knightsInfo[other][1] = c + dj[d]
    # 밀리는 기사 저장
    other_knights = set()
    # 이동 위치
    new_posi = set()
    # 함정 개수
    trap = 0

    for x in range(r, r+h):
        for y in range(c, c+w):
            nx = x + di[d]
            ny = y + dj[d]
            # 벽이 있으면 이동 불가
            if 0 > nx or nx >= l or 0 > ny or ny >= l or graph[nx][ny] == 2:
                # 벽만나서 이동 불가
                return -1

            # 다른 기사가 있으면 다른 기사 번호 저장
            if new_knights[nx][ny] != 0 and new_knights[nx][ny] != other:
                other_knights.add(new_knights[nx][ny])

            # 이동 전 위치 리셋
            new_knights[x][y] = 0
            # 함정 개수 추가
            trap += graph[nx][ny]
            # 이동 위치 저장
            new_posi.add((nx, ny))
            
    # 데미지 추가
    if starter != other:
        new_knightsInfo[other][5] += trap
    # 데미지를 체력 이상으로 받으면 삭제
    if new_knightsInfo[other][4] <= new_knightsInfo[other][5]: 
        del new_knightsInfo[other]
    else:
        # 아니라면 존재하므로 표시
        for x, y in new_posi:
            # 이동 위치에 기사 번호 저장
            new_knights[x][y] = other
    # 밀리는 기사 있으면 보내기
    return other_knights


def move_knight():

    # 밀리는 기사와 움직임 상태 저장
    pushed_knight = deque()
    pushed_knight.append(i)
    # 다른 기사가 있으면 밀기 실행
    while pushed_knight:
        # 이동하면서 위치 변경, 밀리는 기사 번호 또는 벽인지, 이동을 멈추는지 반환
        j = pushed_knight.popleft()
        state = can_move(i, j)
        if state == -1:
            return "stay"
        # 추가
        pushed_knight.extend(deque(state))
    return "move"


l, n, q = map(int, input().split())
# 0은 빈칸, 1은 함정, 2는 벽
graph = [list(map(int, input().split())) for _ in range(l)]
# 기사 정보 (r,c,h,w,k): 위치 (r,c)부터 세로 h, 가로 w인 직사각형, 체력 k
knights = [[0]*l for _ in range(l)]
knightsInfo = dict()

for i in range(1, n+1):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    for x in range(r, r+h):
        for y in range(c, c+w):
            knights[x][y] = i
    # 데미지 추가
    knightsInfo[i] = [r, c, h, w, k, 0]

# 북 동 남 서
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

for _ in range(q):
    i, d = map(int, input().split())
    
    if i not in knightsInfo:
        continue
    new_knights = deepcopy(knights)
    new_knightsInfo = deepcopy(knightsInfo)

    if move_knight() == "move":
        knights = new_knights
        knightsInfo = new_knightsInfo

answer = 0
for key in knightsInfo:
    answer += knightsInfo[key][5]
print(answer)